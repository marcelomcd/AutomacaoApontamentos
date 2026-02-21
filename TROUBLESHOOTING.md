# Guia de Troubleshooting - Automação de Apontamentos

## Problema: "Network Error" ou "Backend não está disponível"

### Sintomas
- Erro "Network Error" ao tentar salvar credenciais
- Erro "Backend não está disponível" ao carregar tarefas
- Nada funciona - não salva, não carrega dados

### Solução

#### 1. Verificar se o Backend está rodando

**Opção A: Usar start.bat (Recomendado)**
```bash
start.bat
```
Isso inicia backend e frontend automaticamente em janelas separadas.

**Opção B: Iniciar manualmente**

Terminal 1 - Backend:
```bash
start_backend.bat
```

Terminal 2 - Frontend:
```bash
start_frontend.bat
```

#### 2. Verificar se as portas estão disponíveis

- **Backend**: Deve estar rodando em `http://localhost:8000`
- **Frontend**: Deve estar rodando em `http://localhost:5173`

Para verificar se o backend está rodando:
- Abra o navegador e acesse: `http://localhost:8000`
- Você deve ver: `{"status":"ok","message":"API de Automação de Apontamentos"}`

Para verificar se o backend está respondendo:
- Acesse: `http://localhost:8000/api/health`
- Você deve ver: `{"status":"ok","message":"Backend está rodando","version":"1.0.0"}`

#### 3. Verificar logs do Backend

No terminal onde o backend está rodando, você deve ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Se não aparecer, há um problema com o backend.

#### 4. Verificar se há erros no console do navegador

1. Abra o navegador (F12)
2. Vá para a aba "Console"
3. Procure por erros em vermelho
4. Erros comuns:
   - `Failed to fetch` - Backend não está rodando
   - `CORS error` - Problema de configuração CORS
   - `Network Error` - Backend não está acessível

#### 5. Verificar dependências

**Backend:**
```bash
# Ative o ambiente virtual
venv\Scripts\activate

# Verifique se as dependências estão instaladas
pip list | findstr "fastapi uvicorn playwright"
```

Se faltar alguma:
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm list
```

Se faltar dependências:
```bash
npm install
```

#### 6. Verificar firewall/antivírus

Alguns firewalls ou antivírus podem bloquear as conexões locais. Verifique se:
- O firewall não está bloqueando a porta 8000
- O antivírus não está bloqueando o Python ou Node.js

#### 7. Verificar se outra aplicação está usando as portas

**Windows:**
```bash
netstat -ano | findstr :8000
netstat -ano | findstr :5173
```

Se aparecer algo, outra aplicação está usando a porta. Feche-a ou mude a porta.

## Problema: "Erro ao salvar credenciais"

### Possíveis causas:
1. Backend não está rodando (veja seção acima)
2. Problema de permissões de arquivo
3. Problema com criptografia

### Solução:
1. Verifique se o backend está rodando
2. Verifique se há permissão para criar arquivos na pasta do projeto
3. Verifique os logs do backend para mais detalhes

## Problema: "Nenhuma tarefa encontrada"

### Possíveis causas:
1. Credenciais não estão salvas
2. Credenciais inválidas
3. Problema de conexão com o site QualiWork
4. Mês/ano selecionado não tem tarefas

### Solução:
1. Salve as credenciais primeiro
2. Verifique se as credenciais estão corretas
3. Verifique sua conexão com a internet
4. Tente outro mês/ano

## Verificação Rápida

Execute este checklist:

- [ ] Backend está rodando? (`http://localhost:8000`)
- [ ] Frontend está rodando? (`http://localhost:5173`)
- [ ] Backend responde ao health check? (`http://localhost:8000/api/health`)
- [ ] Não há erros no console do navegador (F12)
- [ ] Credenciais foram salvas?
- [ ] Internet está funcionando?

## Ainda com problemas?

1. Feche todos os terminais
2. Feche o navegador
3. Execute `start.bat` novamente
4. Aguarde alguns segundos para o backend iniciar
5. Abra o navegador e acesse `http://localhost:5173`
6. Verifique os logs na interface

## Logs Úteis

**Backend (Terminal):**
- Mostra requisições recebidas
- Mostra erros do servidor
- Mostra erros do Playwright

**Frontend (Console do Navegador - F12):**
- Mostra erros de rede
- Mostra erros de JavaScript
- Mostra requisições HTTP

**Interface (Seção Log / Status):**
- Mostra status das operações
- Mostra erros amigáveis
- Mostra progresso da automação
