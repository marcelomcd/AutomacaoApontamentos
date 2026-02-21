# Guia de Migração - PyQt para Interface Web

## O que mudou?

Migramos de uma interface PyQt6 para uma interface web moderna com:
- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite + TypeScript
- **Design**: Moderno, responsivo, com glassmorphism

## Vantagens da Nova Interface

1. **Design Moderno**: Interface web profissional e elegante
2. **Responsiva**: Funciona em qualquer tamanho de tela
3. **Manutenível**: Código separado (backend/frontend)
4. **Escalável**: Fácil adicionar novas funcionalidades
5. **Cross-platform**: Funciona em qualquer sistema operacional

## Como Usar

### 1. Instalar Dependências

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 2. Executar

**Opção Simples:**
```bash
start.bat
```

Isso inicia backend e frontend automaticamente.

### 3. Acessar

Abra no navegador:
```
http://localhost:5173
```

## Funcionalidades Mantidas

Todas as funcionalidades da interface PyQt foram mantidas:
- ✅ Salvar credenciais criptografadas
- ✅ Carregar tarefas do sistema
- ✅ Múltiplos períodos específicos
- ✅ Descrições por dia e turno
- ✅ Executar automação
- ✅ Logs em tempo real

## Melhorias Adicionais

- Interface mais intuitiva
- Feedback visual melhor
- Design moderno e profissional
- Melhor tratamento de erros
- Logs mais organizados

## Arquivos Antigos

Os arquivos PyQt ainda estão disponíveis em:
- `ui/main_window.py` (pode ser removido se não usar mais)
- `main.py` (pode ser removido se não usar mais)

## Suporte

Se tiver problemas:
1. Verifique se backend está rodando (porta 8000)
2. Verifique se frontend está rodando (porta 5173)
3. Veja os logs no console do navegador (F12)
4. Veja os logs do backend no terminal
