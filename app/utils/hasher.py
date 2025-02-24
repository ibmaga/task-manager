from passlib.handlers.scrypt import scrypt


class Hasher:
    def __init__(self, hash_func=scrypt):
        self.hash_func = hash_func

    def hash(self, secret: str) -> str:
        return self.hash_func.hash(secret)

    def verify(self, secret: str, hash_: str) -> bool:
        return self.hash_func.verify(secret, hash_)


hasher = Hasher()
