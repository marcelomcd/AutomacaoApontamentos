"""
Servidor FastAPI para automação de apontamentos.
"""
import sys
import os
from pathlib import Path
import uvicorn

# Adiciona diretório raiz ao path para garantir que os imports funcionem
# Obtém o diretório raiz do projeto (pai do diretório backend)
root_dir = Path(__file__).parent.parent.resolve()
root_dir_str = str(root_dir)

# Adiciona ao PYTHONPATH se ainda não estiver
if root_dir_str not in sys.path:
    sys.path.insert(0, root_dir_str)

# Também adiciona ao PYTHONPATH do ambiente
os.environ['PYTHONPATH'] = root_dir_str + os.pathsep + os.environ.get('PYTHONPATH', '')

# Importa o app diretamente
try:
    from backend.api import app
except ImportError as e:
    print(f"ERRO ao importar backend.api: {e}")
    print(f"Diretorio raiz: {root_dir_str}")
    print(f"PYTHONPATH: {sys.path}")
    raise

if __name__ == "__main__":
    # No Windows, usar reload pode causar problemas com multiprocessing
    # Usar reload=False ou usar reload com reload_includes
    import platform
    use_reload = platform.system() != "Windows"
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=use_reload,
        log_level="info"
    )
