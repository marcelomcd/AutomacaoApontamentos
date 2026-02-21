# Automação de Apontamentos - QualiWork

Aplicação web moderna desenvolvida com React + TypeScript (frontend) e FastAPI (backend) para automatizar o preenchimento de apontamentos de horas no sistema QualiWork.

## Funcionalidades

- **Login Seguro**: Armazena credenciais de forma criptografada usando Fernet
- **Seleção de Tarefas**: Carrega e exibe tarefas disponíveis do sistema automaticamente
- **Preenchimento Automático**: Gera horários aleatórios respeitando intervalos válidos
- **Múltiplos Períodos**: Permite configurar vários períodos específicos com diferentes projetos
- **Descrições Flexíveis**: Descrições separadas para manhã e tarde por período
- **Validações**: Garante que horários gerados respeitam regras de negócio:
  - Intervalo de ~1h entre fim da manhã e início da tarde
  - Total de ~8h de trabalho por dia
- **Interface Moderna**: Interface web responsiva e profissional com glassmorphism
- **Logs em Tempo Real**: Acompanhe o progresso da automação em tempo real

## Requisitos

- Python 3.8 ou superior
- Node.js 18+ e npm
- Playwright (será instalado automaticamente pelo setup.bat ou start.bat)

## Instalação e Uso

### Método Automático (Recomendado)

**Primeira vez ou se quiser reinstalar tudo:**
```bash
setup.bat
```

Isso irá:
- Criar ambiente virtual Python
- Instalar todas as dependências Python
- Instalar navegadores do Playwright
- Instalar dependências Node.js

**Iniciar a aplicação:**
```bash
start.bat
```

O `start.bat` agora é inteligente e:
- ✅ Verifica se o ambiente virtual existe (cria se necessário)
- ✅ Verifica se as dependências Python estão instaladas (instala se necessário)
- ✅ Verifica se as dependências Node.js estão instaladas (instala se necessário)
- ✅ Inicia backend e frontend automaticamente

**Se já tiver tudo instalado, apenas execute:**
```bash
start.bat
```

### Método Manual (Opcional)

Se preferir instalar manualmente:

**1. Criar ambiente virtual e instalar dependências Python:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium
```

**2. Instalar dependências Node.js:**
```bash
cd frontend
npm install
cd ..
```

**3. Iniciar aplicação:**
```bash
start.bat
```

### Iniciar Separadamente (Opcional)

Se quiser iniciar backend e frontend em terminais separados:

Terminal 1 (Backend):
```bash
start_backend.bat
```

Terminal 2 (Frontend):
```bash
start_frontend.bat
```

### Acessar Interface

Abra no navegador:
```
http://localhost:5173
```

### Passo a Passo

1. **Primeira vez**:
   - Preencha seu email e senha nos campos de login
   - Clique em "Salvar Credenciais" (as credenciais serão criptografadas)

2. **Carregar Tarefas**:
   - Selecione mês e ano
   - Clique em "Carregar Tarefas"
   - As tarefas serão carregadas automaticamente e exibidas em uma tabela

3. **Configurar Períodos**:
   - Clique no botão "+" para adicionar um novo período
   - Para cada período:
     - Defina "De" e "Até" (formato DD/MM/AAAA ou DDMMAAAA)
     - Selecione o projeto desejado
     - Preencha descrição para manhã e tarde

4. **Executar Automação**:
   - Clique em "Executar Automação"
   - Acompanhe o progresso na área de logs
   - Ao final, o navegador será exibido para confirmação

## Estrutura do Projeto

```
AutomacaoApontamentos/
├── backend/                     # API FastAPI
│   ├── api.py                   # Endpoints da API
│   └── server.py                # Servidor FastAPI
├── frontend/                    # Interface React
│   ├── src/
│   │   ├── components/          # Componentes React
│   │   ├── services/           # Serviços API
│   │   └── types/              # Definições TypeScript
│   └── package.json
├── automation/
│   ├── playwright_controller.py # Controle do Playwright
│   └── form_filler.py           # Lógica de preenchimento
├── security/
│   └── credential_manager.py    # Gerenciamento de credenciais
├── utils/
│   └── time_generator.py        # Geração de horários
├── requirements.txt
├── start.bat                    # Inicia tudo
└── README.md
```

## Regras de Geração de Horários

A aplicação gera horários aleatórios respeitando os seguintes intervalos:

- **Manhã**:
  - Início: 08:55 - 09:00
  - Fim: 12:00 - 12:15

- **Tarde**:
  - Início: 13:00 - 13:15
  - Fim: 18:00 - 18:15

- **Validações**:
  - Intervalo entre fim manhã e início tarde: 45min a 1h15min (entre 12:00-13:15)
  - Total do dia: aproximadamente 8h (465min a 495min)

## Segurança

- Credenciais são criptografadas usando Fernet (cryptography)
- Chave de criptografia é derivada do sistema do usuário
- Credenciais nunca são armazenadas em texto plano
- Arquivo de credenciais: `.credentials.encrypted`

## Notas Importantes

- A aplicação preenche apenas dias úteis (segunda a sexta)
- Cada dia possui duas entradas: manhã e tarde
- O navegador será exibido ao final para confirmação, mesmo em modo silencioso
- É necessário confirmar e salvar manualmente no sistema após a automação

## Troubleshooting

**Erro ao instalar Playwright:**
```bash
pip install playwright
python -m playwright install chromium
```

**Erro de login:**
- Verifique se as credenciais estão corretas
- Tente salvar as credenciais novamente

**Tarefas não carregam:**
- Verifique sua conexão com a internet
- Verifique se as credenciais estão corretas
- Verifique se o backend está rodando (porta 8000)
- Veja os logs no console do navegador (F12)

**Frontend não carrega:**
- Verifique se Node.js está instalado: `node --version`
- Execute `npm install` na pasta frontend
- Verifique se a porta 5173 está disponível

**Backend não inicia:**
- Verifique se Python está instalado: `python --version`
- Execute `pip install -r requirements.txt`
- Verifique se a porta 8000 está disponível

## Licença

Este projeto é de uso pessoal e não possui licença específica.
