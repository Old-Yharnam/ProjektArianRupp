""" 
Darstellung eines einzelnes Gerätes für klare und übersichtliche Anzeige der Informationen.
"""

from nicegui import ui

class DeviceCard:
    @staticmethod
    def display_device_card(device):
        with ui.card():
            ui.label(f"Gerätename: {getattr(device, 'device_id', 'Unbekannt')}")
            if hasattr(device, 'network_status'):
                ns = device.network_status
                ui.label(f"Signalstärke: {getattr(ns, 'signal_strength', 'N/A')} dBm")
                ui.label(f"Verbindungsqualität: {getattr(ns, 'connection_quality', 'N/A')}")
            else:
                ui.label("Keine Netzwerkdaten verfügbar.")