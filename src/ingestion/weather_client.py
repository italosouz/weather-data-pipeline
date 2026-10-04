import requests
import json
from pathlib import Path
from datetime import datetime, timezone


def fetch_weather(url, params):
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

def save_raw_json(data, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open(mode="w", encoding="utf-8") as weather_file:  
        json.dump(data, weather_file, ensure_ascii=False, indent=2)


def main():
    end_point = 'https://api.open-meteo.com/v1/forecast'
    params = {
        "latitude": -23.5505,
        "longitude": -46.6333,
        "hourly": "temperature_2m",
        "forecast_days": 1,
        "timezone": "America/Sao_Paulo"
    }

    try:
        data = fetch_weather(end_point, params)
    except requests.exceptions.Timeout:
        print("Coleta falhou por timeout")
        raise SystemExit(1)
    except requests.exceptions.HTTPError as exc:
        print(f"Erro na requisição HTTP: {exc}")
        raise SystemExit(1)
    except requests.exceptions.ConnectionError as exc:
        print(f"Não foi possível conectar a api: {exc}")
        raise SystemExit(1)
    
    collected_at = datetime.now(timezone.utc)
    collection_id = collected_at.strftime("%Y%m%dT%H%M%S%fZ")
    output_path = f'data/raw/weather_{collection_id}.json'

    save_raw_json(data, output_path)
    print(f"Coleta salva em: {output_path}")

if __name__ == "__main__":
    main()