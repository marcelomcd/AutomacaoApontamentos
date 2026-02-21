"""
API Backend FastAPI para comunicação com automação Playwright.
Seguindo princípios de arquitetura limpa e SOLID.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import uvicorn
from contextlib import asynccontextmanager

import sys
from pathlib import Path

# Adiciona diretório raiz ao path para imports
root_dir = Path(__file__).parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from automation.playwright_controller import PlaywrightController
from automation.form_filler import FormFiller
from security.credential_manager import CredentialManager


# Modelos Pydantic para validação
class CredentialsRequest(BaseModel):
    email: str
    password: str


class LoadTasksRequest(BaseModel):
    month: int
    year: int


class PeriodData(BaseModel):
    de: str  # DD/MM/AAAA
    ate: str  # DD/MM/AAAA
    task_index: int
    desc_morning: str
    desc_afternoon: str


class ExecuteAutomationRequest(BaseModel):
    periods: List[PeriodData]
    headless: bool = True


# Estado global (singleton para Playwright)
playwright_controller: Optional[PlaywrightController] = None
form_filler: Optional[FormFiller] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia ciclo de vida da aplicação."""
    # Startup
    yield
    # Shutdown
    global playwright_controller
    if playwright_controller:
        await playwright_controller.close()


app = FastAPI(
    title="Automação de Apontamentos API",
    description="API para automação de apontamentos QualiWork",
    version="1.0.0",
    lifespan=lifespan
)

# CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check."""
    return {"status": "ok", "message": "API de Automação de Apontamentos"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint para verificar se o backend está rodando."""
    return {
        "status": "ok",
        "message": "Backend está rodando",
        "version": "1.0.0"
    }


@app.post("/api/credentials/save")
async def save_credentials(request: CredentialsRequest):
    """Salva credenciais criptografadas."""
    try:
        credential_manager = CredentialManager()
        success = credential_manager.save_credentials(request.email, request.password)
        
        if success:
            return {"success": True, "message": "Credenciais salvas com sucesso"}
        else:
            raise HTTPException(status_code=500, detail="Erro ao salvar credenciais")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/credentials/load")
async def load_credentials():
    """Carrega credenciais salvas."""
    try:
        credential_manager = CredentialManager()
        if credential_manager.has_credentials():
            credentials = credential_manager.load_credentials()
            if credentials:
                email, _ = credentials
                return {"success": True, "email": email, "has_credentials": True}
        
        return {"success": True, "has_credentials": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/tasks/load")
async def load_tasks(request: LoadTasksRequest):
    """Carrega tarefas disponíveis do sistema."""
    global playwright_controller
    
    try:
        # Carrega credenciais
        credential_manager = CredentialManager()
        if not credential_manager.has_credentials():
            raise HTTPException(status_code=400, detail="Credenciais não encontradas")
        
        credentials = credential_manager.load_credentials()
        if not credentials:
            raise HTTPException(status_code=400, detail="Erro ao carregar credenciais")
        
        email, password = credentials
        
        # Inicializa Playwright (sempre visível para verificação manual)
        if not playwright_controller:
            playwright_controller = PlaywrightController(headless=False)
            await playwright_controller.initialize()
        else:
            # Reutiliza ou reinicializa se necessário
            try:
                _ = playwright_controller.page.url
            except:
                await playwright_controller.initialize()
        
        # Login
        if not await playwright_controller.login(email, password):
            raise HTTPException(status_code=401, detail="Falha no login")
        
        # Navega para página com mês/ano
        if not await playwright_controller.navigate_to_apontamentos(request.month, request.year):
            raise HTTPException(status_code=500, detail="Erro ao navegar para página")
        
        # Extrai tarefas
        tasks = await playwright_controller.get_available_tasks()
        
        if not tasks:
            raise HTTPException(status_code=404, detail="Nenhuma tarefa encontrada")
        
        return {
            "success": True,
            "tasks": tasks,
            "count": len(tasks)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar tarefas: {str(e)}")


@app.post("/api/automation/execute")
async def execute_automation(request: ExecuteAutomationRequest):
    """Executa automação de preenchimento."""
    global playwright_controller, form_filler
    
    try:
        # Carrega credenciais
        credential_manager = CredentialManager()
        if not credential_manager.has_credentials():
            raise HTTPException(status_code=400, detail="Credenciais não encontradas")
        
        credentials = credential_manager.load_credentials()
        if not credentials:
            raise HTTPException(status_code=400, detail="Erro ao carregar credenciais")
        
        email, password = credentials
        
        # Inicializa Playwright (sempre visível para verificação manual)
        # Ignora request.headless e sempre mostra o navegador
        if not playwright_controller:
            playwright_controller = PlaywrightController(headless=False)
            await playwright_controller.initialize()
        
        # Login
        if not await playwright_controller.login(email, password):
            raise HTTPException(status_code=401, detail="Falha no login")
        
        # Inicializa FormFiller
        form_filler = FormFiller(playwright_controller)
        
        # Processa cada período
        all_results = {
            'success': True,
            'filled_dates': [],
            'errors': [],
            'total_entries': 0
        }
        
        for period in request.periods:
            # Converte strings de data para datetime
            try:
                de_date = datetime.strptime(period.de, '%d/%m/%Y')
                ate_date = datetime.strptime(period.ate, '%d/%m/%Y')
            except:
                all_results['errors'].append(f"Data inválida: {period.de} - {period.ate}")
                continue
            
            # Executa preenchimento
            results = await form_filler.fill_date_range(
                de_date,
                ate_date,
                period.task_index,
                period.desc_morning,
                period.desc_afternoon
            )
            
            # Agrega resultados
            if not results['success']:
                all_results['success'] = False
            
            all_results['filled_dates'].extend(results['filled_dates'])
            all_results['errors'].extend(results['errors'])
            all_results['total_entries'] += results['total_entries']
        
        return all_results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na automação: {str(e)}")


@app.get("/api/automation/status")
async def get_automation_status():
    """Retorna status da automação."""
    global playwright_controller
    
    browser_open = False
    if playwright_controller:
        try:
            # Verifica se a página existe e está inicializada
            browser_open = playwright_controller.page is not None and playwright_controller._initialized
        except:
            browser_open = False
    
    return {
        "playwright_initialized": playwright_controller is not None,
        "browser_open": browser_open
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
