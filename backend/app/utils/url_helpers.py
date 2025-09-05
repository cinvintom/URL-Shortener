import random
import string
from app.core.config import settings


class URLUtils:
    @staticmethod
    def generate_random_short_url(length: int = settings.SHORT_URL_LENGTH) -> str:
        """
        Generate a random short URL string.

        Parameters:
            length (int): Desired length of the generated short URL. Defaults to settings.SHORT_URL_LENGTH.

        Returns:
            str: Randomly generated short URL consisting of ASCII letters and digits.
        """
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=length))
