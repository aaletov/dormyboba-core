from dataclasses import dataclass
import random
import base64
import jwt
from cryptography.hazmat.primitives import serialization

@dataclass
class Token:
    role: str
    random_id: int

    @staticmethod
    def generate(role: str) -> 'Token':
        random_id = random.randint(100000, 999999)
        return Token(
            role=role,
            random_id=random_id,
        )

class TokenConverter:
    def __init__(self, private_key: str):
        self.private_key = serialization.load_pem_private_key(
            data=private_key.encode("utf-8"),
            password=None,
        )
        self.public_key = self.private_key.public_key()

    def encode(self, token: Token) -> str:
        once_encoded = jwt.encode({
            "role": token.role,
            "random_id": token.random_id,
        }, key=self.private_key, algorithm="RS256")

        return base64.b64encode(once_encoded.encode("utf-8")).decode("utf-8")

    def decode(self, token: str) -> Token:
        once_encoded = base64.b64decode(token.encode("utf-8"))
        decoded = jwt.decode(once_encoded, key=self.public_key, algorithms=["RS256"])

        return Token(
            role=decoded["role"],
            random_id=decoded["random_id"],
        )
