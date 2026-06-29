""" 
Definiert Sensordaten als Datenklasse, die Informationen über die Sensor-ID,
den Zeitstempel und die gemessenen Werte enthält.
"""

class SensorData:
    def __init__(self, sensor_id, timestamp, values):
        self.sensor_id = sensor_id
        self.timestamp = timestamp
        self.values = values

    def __repr__(self):
        return f"SensorData(sensor_id={self.sensor_id}, timestamp={self.timestamp}, values={self.values})"