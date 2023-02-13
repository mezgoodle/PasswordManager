from cryptography.fernet import Fernet

from tgbot.config import config


class Crypter:
    def __init__(self):
        self.fernet = Fernet(config.FERNET_KEY.get_secret_value())

    def encrypt(self, text: str) -> str:
        """Method for encrypting text

        Args:
            text (str): text to encrypt

        Returns:
            str: encrypted text
        """
        return self.fernet.encrypt(text.encode()).decode()

    def decrypt(self, encrypted_text: str) -> str:
        """Method for decrypting text

        Args:
            encrypted_text (str): text for decrypt

        Returns:
            str: decrypted text
        """
        return self.fernet.decrypt(encrypted_text).decode()
