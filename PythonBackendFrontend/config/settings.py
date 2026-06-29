"""
Hier werden alle Einstellungen und Konstanten definiert, 
die im gesamten Projekt verwendet werden um Magic Numbers zu vermeiden und die Wartbarkeit zu erhöhen.
"""

# MQTT Broker Einstellungen
MQTT_BROKER_HOST = '10.43.132.71'
MQTT_BROKER_PORT = 1883
MQTT_BROKER_USERNAME = 'mqtt_broker_aru7063'
MQTT_BROKER_PASSWORD = '************'

# MQTT Topics
MQTT_TOPIC_COMMANDS = 'esp/sensor/commands'
MQTT_TOPIC_SENSOR = 'sensor/hw201/status'