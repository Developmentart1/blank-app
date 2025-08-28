import os

class Settings:
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg://analytics:analytics@localhost:5432/analytics")
    tz: str = os.getenv("TZ", "America/Mazatlan")
    alert_amber: float = float(os.getenv("ALERT_AMBER", 0.05))
    alert_orange: float = float(os.getenv("ALERT_ORANGE", 0.10))
    alert_red: float = float(os.getenv("ALERT_RED", 0.20))

settings = Settings()
