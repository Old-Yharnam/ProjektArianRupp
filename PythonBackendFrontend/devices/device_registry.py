""" 
Verwaltet alle Geräte im System.
Es ermöglicht das Hinzufügen, Entfernen und Abrufen von Geräten basierend auf ihrer ID oder ihrem Namen. 
Alle Geräte werden in einem Dictionary gespeichert, wobei die Schlüssel die eindeutigen IDs der Geräte sind.
"""

import devices.device as device

class DeviceRegistry:
    def __init__(self):
        self.devices = {}

    def add_device(self, device: device.Device):
        """Fügt ein neues Gerät zum Registry hinzu."""
        self.devices[device.device_id] = device

    def remove_device(self, device_id: str):
        """Entfernt ein Gerät aus dem Registry basierend auf seiner ID."""
        if device_id in self.devices:
            del self.devices[device_id]

    def get_device_by_id(self, device_id: str) -> device.Device:
        """Gibt ein Gerät basierend auf seiner ID zurück."""
        return self.devices.get(device_id)

    def get_device_by_name(self, name: str) -> device.Device:
        """Gibt ein Gerät basierend auf seinem Namen zurück."""
        for device in self.devices.values():
            if getattr(device, 'name', device.device_id) == name:
                return device
        return None

    def get_device(self, device_id: str) -> device.Device:
        """Kompatibilitätsmethode für älteren Aufrufstil."""
        return self.get_device_by_id(device_id)