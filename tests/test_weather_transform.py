import unittest
from src.transformation.weather_transform import transform_weather

class TestTransformWeather(unittest.TestCase):
    def test_transforma_resposta_valida(self):
        data = {
            "latitude": -23.55,
            "longitude": -46.63,
            "timezone": "America/Sao_Paulo",
            "hourly": {
                "time": ["2026-10-04T00:00", "2026-10-04T01:00"],
                "temperature_2m": [17.4, 17.2],
            },
        }

        records = transform_weather(data)

        self.assertEqual(len(records), 2)
        self.assertEqual(
            records[0],
            {
                "forecast_time": "2026-10-04T00:00",
                "temperature_2m": 17.4,
                "latitude": -23.55,
                "longitude": -46.63,
                "timezone": "America/Sao_Paulo",
            },
        )

    def test_rejeita_lista_tamanhos_diferentes(self):
        data = {
            "latitude": -23.55,
            "longitude": -46.63,
            "timezone": "America/Sao_Paulo",
            "hourly": {
                "time": ["2026-10-04T00:00", "2026-10-04T01:00"],
                "temperature_2m": [17.4],
            },
        }
         
        with self.assertRaises(ValueError):
            transform_weather(data)

    def test_rejeita_lista_vazia(self):
        data = {
            "latitude": -23.55,
            "longitude": -46.63,
            "timezone": "America/Sao_Paulo",
            "hourly": {
                "time": [],
                "temperature_2m": [],
            },
        }
            
        with self.assertRaises(ValueError):
            transform_weather(data)


if __name__ == "__main__":
    unittest.main()
