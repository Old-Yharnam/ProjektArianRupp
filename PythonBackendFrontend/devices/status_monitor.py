""" 
Überwacht den Status aller Geräte und gibt diesenfalls an die Benutzeroberfläche weiter.
"""

import devices.device_registry as device_registry

class StatusMonitor:
    def __init__(self):
        self.device_registry = device_registry.DeviceRegistry()

    def get_device_status(self, device_id):
        device = self.device_registry.get_device_by_id(device_id)
        if device:
            return device.get_status()
        else:
            return None