from datetime import datetime, timezone
from zoneinfo import ZoneInfo

texto = "2026-10-04T00:00"

converted = datetime.fromisoformat(texto)
print(converted)
fuso = converted.replace(tzinfo=ZoneInfo("America/Sao_Paulo"))
print("fuso associado", fuso)

utc = fuso.astimezone(timezone.utc)
print("utc", utc)
