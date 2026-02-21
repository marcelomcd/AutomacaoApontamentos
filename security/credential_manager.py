"""
Gerenciador de credenciais com criptografia segura.
Armazena email e senha de forma criptografada usando Fernet.
"""
import os
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class CredentialManager:
    """Gerencia credenciais de forma segura usando criptografia."""
    
    def __init__(self, credentials_file: str = ".credentials.encrypted"):
        """
        Inicializa o gerenciador de credenciais.
        
        Args:
            credentials_file: Nome do arquivo para armazenar credenciais criptografadas
        """
        self.credentials_file = Path(credentials_file)
        self._fernet = None
        self._initialize_fernet()
    
    def _initialize_fernet(self):
        """Inicializa o objeto Fernet com chave derivada do sistema."""
        # Deriva chave única baseada no usuário do sistema
        # Usa uma combinação de informações do sistema para criar uma chave única
        system_key = self._derive_system_key()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'qualiwork_salt_2025',  # Salt fixo para consistência
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(system_key.encode()))
        self._fernet = Fernet(key)
    
    def _derive_system_key(self) -> str:
        """
        Deriva uma chave única baseada no sistema.
        Usa nome de usuário e caminho do diretório home.
        """
        username = os.getlogin() if hasattr(os, 'getlogin') else os.getenv('USERNAME', 'default_user')
        home = os.path.expanduser('~')
        # Combina informações para criar chave única
        system_key = f"{username}_{home}_qualiwork_2025"
        return system_key
    
    def save_credentials(self, email: str, password: str) -> bool:
        """
        Salva credenciais de forma criptografada.
        
        Args:
            email: Email do usuário
            password: Senha do usuário
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            credentials_data = f"{email}|||{password}"
            encrypted_data = self._fernet.encrypt(credentials_data.encode())
            
            # Salva em arquivo
            with open(self.credentials_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Define permissões restritas (apenas leitura para o dono)
            if os.name != 'nt':  # Unix-like
                os.chmod(self.credentials_file, 0o600)
            
            return True
        except Exception as e:
            print(f"Erro ao salvar credenciais: {e}")
            return False
    
    def load_credentials(self) -> tuple[str, str] | None:
        """
        Carrega credenciais descriptografadas.
        
        Returns:
            Tupla (email, password) ou None se não encontrar/erro
        """
        try:
            if not self.credentials_file.exists():
                return None
            
            with open(self.credentials_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self._fernet.decrypt(encrypted_data)
            credentials_data = decrypted_data.decode()
            email, password = credentials_data.split('|||')
            
            return email, password
        except Exception as e:
            print(f"Erro ao carregar credenciais: {e}")
            return None
    
    def has_credentials(self) -> bool:
        """
        Verifica se existem credenciais salvas.
        
        Returns:
            True se existem credenciais salvas, False caso contrário
        """
        return self.credentials_file.exists()
    
    def delete_credentials(self) -> bool:
        """
        Remove credenciais salvas.
        
        Returns:
            True se removeu com sucesso, False caso contrário
        """
        try:
            if self.credentials_file.exists():
                self.credentials_file.unlink()
            return True
        except Exception as e:
            print(f"Erro ao deletar credenciais: {e}")
            return False
