CONF_HOST = "host"
CONF_PORT = "port"
CONF_UNIT_ID = "unit_id"

POLLING_INTERVAL = 5
DOMAIN = "powerbox"
MODBUS_REGISTERS = [
    {
        "unique_id": "room_temperature",
        "address": 700,
        "length": 1,
        "scale": 0.1,
        "precision": 1
    },
    {
        "unique_id": "outside_temperature",
        "address": 703,
        "length": 1,
        "scale": 0.1,
        "precision": 1
    },
    {
        "unique_id": "air_humidity",
        "address": 750,
        "length": 1,
    },
    {
        "unique_id": "operating_mode",
        "address": 550,
        "length": 1,
        "scale": 1,
        "precision": 0
    },
    {
        "unique_id": "ventilation_level",
        "address": 554,
        "length": 1,
        "scale": 1,
        "precision": 0
    },
    {
        "unique_id": "purge_ventilation",
        "address": 551,
        "length": 1,
        "scale": 1,
        "precision": 0
    },
    {
        "unique_id": "sleep_function",
        "address": 559,
        "length": 1,
        "scale": 1,
        "precision": 0
    }
]

ENTITIES = [
    {
        "type": "sensor",
        "name": "Raumtemperatur",
        "icon": "mdi:thermometer",
        "unique_id": "room_temperature",
        "device_class": "temperature",
        "state_class": "Measurement",
        "unit_of_measurement": "°C",
        "modbus_address": 700,
        "modbus_length": 1,
        "scale": 0.1,
        "precision": 1
    },
    {
        "type": "sensor",
        "name": "Aussentemperatur",
        "icon": "mdi:thermometer",
        "unique_id": "outside_temperature",
        "device_class": "temperature",
        "state_class": "Measurement",
        "unit_of_measurement": "°C",
        "modbus_address": 703,
        "modbus_length": 1,
        "scale": 0.1,
        "precision": 1
    },
    {
        "type": "sensor",
        "name": "Luftfeuchtigkeit",
        "icon": "mdi:water-percent",
        "unique_id": "air_humidity",
        "device_class": "humidity",
        "state_class": "Measurement",
        "unit_of_measurement": "%",
        "modbus_address": 750,
        "modbus_length": 1,
    },
    {
        "type": "sensor",
        "name": "Betriebsart",
        "icon": "",
        "unique_id": "operating_mode",
        "state_class": "Measurement",
        "modbus_address": 550,
        "modbus_length": 1,
        "scale": 1,
        "precision": 0
    },
    {
        "type": "sensor",
        "name": "Luftungsstufe",
        "icon": "",
        "unique_id": "ventilation_level",
        "modbus_address": 554,
        "modbus_length": 1,
        "scale": 1,
        "precision": 0
    },
    {
        "type": "binary_sensor",
        "name": "Stossluftung",
        "icon": "",
        "unique_id": "purge_ventilation",
        "modbus_address": 551,
        "modbus_length": 1,
        "scale": 1,
        "precision": 0
    },
    {
        "type": "binary_sensor",
        "name": "Einschlaffunktion",
        "icon": "",
        "unique_id": "sleep_function",
        "modbus_address": 559,
        "modbus_length": 1,
        "scale": 1,
        "precision": 0
    }
]
