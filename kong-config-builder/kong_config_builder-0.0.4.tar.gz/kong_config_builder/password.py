import string
import secrets


class PasswordManager:
    @staticmethod
    def generate(size: int) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for i in range(int(size)))
