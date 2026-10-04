import json
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq

def transform_weather(data):
    times = data['hourly']['time']
    temps = data['hourly']['temperature_2m']

    records = []
    if len(times) == len(temps):
        if len(times) == 0: 
            raise ValueError("Lista de horários vazia") 
        
        for forecast_time, temperature in zip(times, temps):
            records.append({
                "forecast_time": forecast_time,
                "temperature_2m": temperature,
                "latitude": data["latitude"],
                "longitude": data["longitude"],
                "timezone": data["timezone"]
            })
    else:
        raise ValueError("Quantidade de horários diferente da quantidade de temperaturas")

    return records

def save_bronze_parquet(records, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    schema = pa.schema([
        ("forecast_time", pa.string()),
        ("temperature_2m", pa.float64()),
        ("latitude", pa.float64()),
        ("longitude", pa.float64()),
        ("timezone", pa.string())
    ])

    table = pa.Table.from_pylist(records, schema=schema)
    pq.write_table(table, output_path)

def main():
    weather_path = "data/raw/weather_20261004T182740376788Z.json"
    with open(weather_path, mode="r", encoding="utf-8") as weather_file:
        data = json.load(weather_file)

    records = transform_weather(data)
    # print(records[0])
    # print("Total de registros:", len(records))
    
    output_path = Path("data/bronze") / Path(weather_path).with_suffix(".parquet").name
    save_bronze_parquet(records, output_path)
    print(f"Arquivo parquet salvo em: {output_path}")

    # saved_table = pq.read_table(output_path)
    # print(saved_table.schema)
    # print("Linhas gravadas:", saved_table.num_rows)
    # print(
    #     "Conteúdo preservado:",
    #     saved_table.to_pylist() == records,
    # )
if __name__ == "__main__":
    main()