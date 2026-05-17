import os

class Settings:
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY", "CHANGE_ME_MARS_SECRET")
        self.algorithm = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

settings = Settings()
