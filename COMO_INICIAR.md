# Como Iniciar a Aplicação

## Método Simples (Recomendado)

### Primeira Vez

Execute o script de configuração:

```bash
setup.bat
```

Isso irá:
1. Criar ambiente virtual Python
2. Instalar todas as dependências Python
3. Instalar navegadores do Playwright
4. Instalar dependências Node.js

### Iniciar Aplicação

Execute apenas um arquivo:

```bash
start.bat
```

O `start.bat` agora é inteligente e:
1. ✅ Verifica se Python e Node.js estão instalados
2. ✅ Cria ambiente virtual se não existir
3. ✅ Instala dependências Python se necessário
4. ✅ Instala dependências Node.js se necessário
5. ✅ Inicia o Backend automaticamente (porta 8000)
6. ✅ Aguarda 5 segundos
7. ✅ Inicia o Frontend automaticamente (porta 5173)
8. ✅ Abre duas janelas separadas (uma para cada servidor)

**Se já tiver tudo instalado, apenas execute `start.bat` - ele detecta automaticamente o que falta!**

## O que acontece quando você executa start.bat

### Janela 1: Backend
- Ativa o ambiente virtual (se existir)
- Verifica dependências
- Inicia o servidor FastAPI em `http://localhost:8000`
- Mostra logs em tempo real

### Janela 2: Frontend
- Verifica se Node.js está instalado
- Instala dependências se necessário (`npm install`)
- Inicia o servidor Vite em `http://localhost:5173`
- Mostra logs em tempo real

### Janela Principal
- Mostra status de inicialização
- Informa as URLs de acesso
- Pode ser fechada após iniciar

## Verificar se está funcionando

### Backend
Abra no navegador: `http://localhost:8000`

Você deve ver:
```json
{"status":"ok","message":"API de Automação de Apontamentos"}
```

### Frontend
Abra no navegador: `http://localhost:5173`

Você deve ver a interface da aplicação.

### Health Check
Abra no navegador: `http://localhost:8000/api/health`

Você deve ver:
```json
{"status":"ok","message":"Backend está rodando","version":"1.0.0"}
```

## Problemas Comuns

### "Python não encontrado"
- Instale Python 3.8 ou superior
- Adicione Python ao PATH do sistema

### "Node.js não encontrado"
- Instale Node.js 18 ou superior
- Adicione Node.js ao PATH do sistema

### "Backend não inicia"
1. Execute `test_backend.bat` para diagnosticar
2. Verifique se as dependências estão instaladas:
   ```bash
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Verifique os logs na janela do backend

### "Frontend não inicia"
1. Verifique se Node.js está instalado: `node --version`
2. Instale dependências manualmente:
   ```bash
   cd frontend
   npm install
   ```
3. Verifique os logs na janela do frontend

### "Porta já em uso"
- Feche outras aplicações usando as portas 8000 ou 5173
- Ou mude as portas nos arquivos de configuração

## Testar Backend Separadamente

Se quiser testar apenas o backend:

```bash
test_backend.bat
```

Isso verifica:
- Se o backend pode ser importado
- Se as dependências estão instaladas
- Se há erros de configuração

## Estrutura dos Arquivos .bat

- **start.bat**: Inicia tudo (backend + frontend)
- **start_backend.bat**: Inicia apenas o backend
- **start_frontend.bat**: Inicia apenas o frontend
- **test_backend.bat**: Testa se o backend está configurado corretamente

## Dicas

1. **Primeira vez**: Execute `start.bat` e aguarde alguns segundos para tudo iniciar
2. **Verificar logs**: As janelas do backend e frontend mostram logs em tempo real
3. **Fechar**: Feche as janelas do backend/frontend para parar os servidores
4. **Reiniciar**: Feche tudo e execute `start.bat` novamente

## Próximos Passos

Após iniciar:
1. Acesse `http://localhost:5173` no navegador
2. Salve suas credenciais
3. Carregue as tarefas
4. Configure os períodos
5. Execute a automação
