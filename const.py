CONF_HOST = "host"
CONF_PORT = "port"
CONF_UNIT_ID = "unit_id"
POLLING_INTERVAL = 5
DOMAIN = "powerbox"
MODBUS_REGISTERS = [
    {
        "localized_name": "Temperatur Raum",
        "unique_id": "room_temperature",
        "address": 700,
        "length": 1,
        "scale": 0.1,
        "precision": 1
    },
    {
        "localized_name": "Temperatur Lufteintritt",
        "unique_id": "outside_temperature",
        "address": 703,
        "length": 1,
        "scale": 0.1,
        "precision": 1
    },
    {
        "localized_name": "Temperatur Zuluft",
        "unique_id": "supply_air_temperature",
        "address": 704,
        "length": 1,
        "scale": 0.1,
        "precision": 0
    },
    {
        "localized_name": "Temperatur Abluft",
        "unique_id": "exhaust_air_temperature",
        "address": 705,
        "length": 1,
        "scale": 0.1,
        "precision": 0
    },
    {
        "localized_name": "Temperatur Fortluft",
        "unique_id": "discharge_air_temperature",
        "address": 706,
        "length": 1,
        "scale": 0.1,
        "precision": 0
    },
    {
        "localized_name": "Luftfeuchtigkeit",
        "unique_id": "air_humidity",
        "address": 750,
        "length": 1,
    },
    {
        "localized_name": "Betriebsart",
        "unique_id": "operating_mode",
        "address": 550,
        "length": 1,
        "scale": 1,
        "precision": 0
    },
    {
        "localized_name": "Lüftungsstufe",
        "unique_id": "ventilation_level",
        "address": 554,
        "length": 1,
        "scale": 1,
        "precision": 0
    },
    {
        "localized_name": "Stoßlüftung",
        "unique_id": "purge_ventilation",
        "address": 551,
        "length": 1,
        "scale": 1,
        "precision": 0
    },
    {
        "localized_name": "Einschlaffunktion",
        "unique_id": "sleep_function",
        "address": 559,
        "length": 1,
        "scale": 1,
        "precision": 0
    },
    {
        "localized_name": "Volumenstrom Zuluft",
        "unique_id": "volume_flow_supply",
        "address": 653,
        "length": 1,
        "scale": 1,
        "precision": 0
    },
    {
        "localized_name": "Volumenstrom Abluft",
        "unique_id": "volume_flow_exhaust",
        "address": 654,
        "length": 1,
        "scale": 1,
        "precision": 0
    },
    {
        "localized_name": "Aktueller Fehler",
        "unique_id": "error",
        "address": 401,
        "length": 2
    },
    {
        "localized_name": "Aktueller Hinweis",
        "unique_id": "remark",
        "address": 403,
        "length": 2
    },
]
def get_localized_name(unique_id):
    for item in MODBUS_REGISTERS:
        if item.get("unique_id") == unique_id:
            return item.get("localized_name")