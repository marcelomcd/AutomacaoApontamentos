@echo off
title Automação de Apontamentos - Iniciar Tudo
color 0A
echo ========================================
echo   Automação de Apontamentos
echo   Iniciando Aplicação Completa
echo ========================================
echo.

REM Garante que está no diretório correto
cd /d "%~dp0"
set PROJECT_DIR=%CD%
echo Diretório do projeto: %PROJECT_DIR%
echo.

REM ========================================
REM 1. VERIFICAÇÃO DE PRÉ-REQUISITOS
REM ========================================
echo [1/7] Verificando pré-requisitos...
echo.

REM Verifica Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado!
    echo Por favor, instale Python 3.8 ou superior.
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [OK] Python encontrado: %PYTHON_VERSION%
)

REM Verifica Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Node.js não encontrado!
    echo Por favor, instale Node.js 18 ou superior.
    pause
    exit /b 1
) else (
    for /f %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
    echo [OK] Node.js encontrado: %NODE_VERSION%
)

echo.

REM ========================================
REM 2. AMBIENTE VIRTUAL PYTHON
REM ========================================
echo [2/7] Configurando ambiente virtual Python...
echo.

if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar ambiente virtual!
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtual criado.
) else (
    echo [OK] Ambiente virtual já existe.
)

REM Ativa ambiente virtual
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRO] Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)

REM Define comando Python do venv
if exist "venv\Scripts\python.exe" (
    set PYTHON_CMD=venv\Scripts\python.exe
) else (
    set PYTHON_CMD=python
)

echo [OK] Ambiente virtual ativado.
echo.

REM ========================================
REM 3. INSTALAÇÃO DE DEPENDÊNCIAS PYTHON
REM ========================================
echo [3/7] Instalando dependências Python...
echo.

REM Atualiza pip
%PYTHON_CMD% -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [AVISO] Falha ao atualizar pip, continuando...
)

REM Verifica se requirements.txt existe
if not exist "requirements.txt" (
    echo [ERRO] Arquivo requirements.txt não encontrado!
    pause
    exit /b 1
)

REM Verifica se as dependências já estão instaladas
%PYTHON_CMD% -c "import fastapi, uvicorn, playwright, cryptography" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependências do requirements.txt...
    %PYTHON_CMD% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependências Python!
        pause
        exit /b 1
    )
    echo [OK] Dependências Python instaladas.
    
    REM Instala navegadores do Playwright
    echo Instalando navegadores do Playwright...
    %PYTHON_CMD% -m playwright install chromium
    if errorlevel 1 (
        echo [AVISO] Falha ao instalar navegadores do Playwright.
        echo Você pode instalar manualmente depois com: python -m playwright install chromium
    )
) else (
    echo [OK] Dependências Python já instaladas.
)

echo.

REM ========================================
REM 4. VERIFICAÇÃO ESTRUTURA BACKEND
REM ========================================
echo [4/7] Verificando estrutura do backend...
echo.

REM Verifica arquivos essenciais do backend
set BACKEND_OK=1

if not exist "backend\server.py" (
    echo [ERRO] backend\server.py não encontrado!
    set BACKEND_OK=0
)

if not exist "backend\api.py" (
    echo [ERRO] backend\api.py não encontrado!
    set BACKEND_OK=0
)

if not exist "automation\playwright_controller.py" (
    echo [ERRO] automation\playwright_controller.py não encontrado!
    set BACKEND_OK=0
)

if not exist "automation\form_filler.py" (
    echo [ERRO] automation\form_filler.py não encontrado!
    set BACKEND_OK=0
)

if not exist "security\credential_manager.py" (
    echo [ERRO] security\credential_manager.py não encontrado!
    set BACKEND_OK=0
)

if %BACKEND_OK%==0 (
    echo [ERRO] Estrutura do backend incompleta!
    pause
    exit /b 1
)

echo [OK] Estrutura do backend verificada.

REM Testa importação do backend
echo Testando importação do backend...
%PYTHON_CMD% -c "import sys; sys.path.insert(0, '.'); from backend.api import app; print('[OK] Backend pode ser importado')" 2>nul
if errorlevel 1 (
    echo [AVISO] Backend não pôde ser importado, mas continuando...
    echo Isso pode ser normal se houver dependências faltando.
) else (
    echo [OK] Backend pode ser importado corretamente.
)

echo.

REM ========================================
REM 5. INSTALAÇÃO E VERIFICAÇÃO FRONTEND
REM ========================================
echo [5/7] Configurando frontend...
echo.

REM Verifica estrutura do frontend
if not exist "frontend\package.json" (
    echo [ERRO] frontend\package.json não encontrado!
    pause
    exit /b 1
)

if not exist "frontend\src" (
    echo [ERRO] Diretório frontend\src não encontrado!
    pause
    exit /b 1
)

echo [OK] Estrutura do frontend verificada.

REM Verifica e instala dependências Node.js
cd frontend

if not exist "node_modules" (
    echo Instalando dependências Node.js...
    call npm install
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependências Node.js!
        cd ..
        pause
        exit /b 1
    )
    echo [OK] Dependências Node.js instaladas.
) else (
    echo [OK] Dependências Node.js já instaladas.
)

REM Verifica se o frontend pode ser executado (testa se vite está disponível)
echo Verificando se Vite está disponível...
call npm list vite >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Vite pode não estar instalado corretamente.
    echo Tentando reinstalar...
    call npm install
) else (
    echo [OK] Vite está disponível.
)

cd ..

echo.

REM ========================================
REM 6. VERIFICAÇÃO FINAL DE FUNCIONAMENTO
REM ========================================
echo [6/7] Verificação final de funcionamento...
echo.

REM Testa se backend pode iniciar (sem realmente iniciar)
echo Testando backend...
%PYTHON_CMD% -c "import sys; sys.path.insert(0, '.'); from backend.api import app; print('[OK] Backend está funcional')" 2>nul
if errorlevel 1 (
    echo [AVISO] Backend pode ter problemas, mas tentando iniciar mesmo assim...
) else (
    echo [OK] Backend está pronto para executar.
)

REM Testa se frontend pode iniciar (verifica se npm run dev existe)
echo Testando frontend...
cd frontend
findstr /C:"\"dev\"" package.json >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Script 'dev' não encontrado no package.json!
    cd ..
    pause
    exit /b 1
) else (
    echo [OK] Frontend está pronto para executar.
)
cd ..

echo.

REM ========================================
REM 7. INICIANDO SERVIDORES
REM ========================================
echo [7/7] Iniciando servidores...
echo.

REM Inicia backend em nova janela
echo Iniciando Backend na porta 8000...
start "Backend API - Automação de Apontamentos" cmd /k "cd /d %PROJECT_DIR% && call venv\Scripts\activate.bat && %PYTHON_CMD% backend\server.py"

REM Aguarda backend iniciar
echo Aguardando backend iniciar (5 segundos)...
ping 127.0.0.1 -n 6 >nul

REM Inicia frontend em nova janela
echo Iniciando Frontend na porta 5173...
cd frontend
start "Frontend - Automação de Apontamentos" cmd /k "cd /d %PROJECT_DIR%\frontend && call npm run dev"
cd ..

echo.
echo ========================================
echo   Servidores Iniciados com Sucesso!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Verifique as janelas abertas para ver os logs.
echo.
echo Pressione qualquer tecla para fechar esta janela...
pause >nul
