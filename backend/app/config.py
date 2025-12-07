from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = ".."
    OPENAI_API_KEY: str = ""
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASS: str = ""

    IMAP_HOST: str = "imap.gmail.com"
    IMAP_USER: str = ""
    IMAP_PASS: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
