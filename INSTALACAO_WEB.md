# Guia de Instalação - Interface Web

## Pré-requisitos

1. **Python 3.8+** instalado
2. **Node.js 18+** instalado (com npm)
3. **Playwright** instalado

## Passo a Passo

### 1. Instalar Dependências Python (Backend)

```bash
# Ative ambiente virtual (se usar)
venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt

# Instale navegadores do Playwright
python -m playwright install chromium
```

### 2. Instalar Dependências Node.js (Frontend)

```bash
cd frontend
npm install
```

### 3. Executar Aplicação

**Opção A: Tudo de uma vez**
```bash
start.bat
```

**Opção B: Separadamente**

Terminal 1 (Backend):
```bash
start_backend.bat
```

Terminal 2 (Frontend):
```bash
start_frontend.bat
```

### 4. Acessar Interface

Abra no navegador:
```
http://localhost:5173
```

## Verificação

- Backend rodando: http://localhost:8000
- Frontend rodando: http://localhost:5173
- API Docs: http://localhost:8000/docs

## Estrutura

```
AutomacaoApontamentos/
├── backend/           # API FastAPI
│   ├── api.py
│   └── server.py
├── frontend/          # Interface React
│   ├── src/
│   └── package.json
├── automation/        # Lógica Playwright
├── security/          # Criptografia
└── utils/             # Utilitários
```

## Problemas Comuns

**Erro: Module not found**
- Verifique se está no diretório correto
- Execute `pip install -r requirements.txt` novamente

**Erro: Port already in use**
- Feche outras instâncias
- Ou mude a porta no código

**Frontend não carrega**
- Verifique se Node.js está instalado: `node --version`
- Execute `npm install` na pasta frontend
