from pathlib import Path
import pyarrow.parquet as pq
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def transform_silver(records):
    silver_records = []
    for record in records:
        converted_isoformat = datetime.fromisoformat(record['forecast_time'])
        assoc_fuso = converted_isoformat.replace(tzinfo=ZoneInfo(record['timezone']))
        utc_time = assoc_fuso.astimezone(timezone.utc)

        silver_records.append({
            **record,
            "forecast_time_utc": utc_time
        })

    return silver_records

def main():
    bronze_path = Path("data/bronze") / "weather_20261004T182740376788Z.parquet"
    records = pq.read_table(bronze_path).to_pylist()
    silver_records = transform_silver(records)
    print(silver_records[0])

if __name__ == "__main__":
    main()