""" 
Die Hauptoberfläche der Anwendung.
"""

from nicegui import ui
import ui.charts as charts
import ui.device_card as device_card
import mqtt.message_handler as message_handler
from models.network_status import NetworkStatus

class Dashboard:
    @staticmethod
    def display_dashboard(device_registry=None, topic_manager=None):
        with ui.card():
            ui.label("Willkommen zum Netzwerkstatus-Dashboard!")
            ui.label("Hier können Sie den aktuellen Status Ihrer Geräte und Verbindungen einsehen.")

            if topic_manager is not None:
                topic = topic_manager.get_topic("ESP-Sensor")
                ui.label(f"Konfiguriertes Command-Topic: {topic}")

        if device_registry is not None:
            Dashboard().display_device_status(list(device_registry.devices.values()))

        Dashboard().display_charts(NetworkStatus(signal_strength=-65, connection_quality="Gut"))

        with ui.card().classes('w-full'):
            ui.label("HW-201 Sensor").classes('text-lg font-bold')
            status_label = ui.label("Warte auf Sensordaten...").classes('text-grey')
            count_label = ui.label("")

            def refresh():
                msgs = message_handler.sensor_messages
                if msgs:
                    status_label.set_text(f"Letztes Ereignis: {msgs[-1]}")
                    status_label.classes(remove='text-grey', add='text-positive')
                    count_label.set_text(f"Gesamte Auslösungen: {len(msgs)}")

            ui.timer(1.0, refresh)
            
    def display_device_status(self, devices):
        with ui.card():
            ui.label("Gerätestatus:")
            for device in devices:
                device_card.DeviceCard.display_device_card(device)
                
    def display_charts(self, network_status):
        with ui.card():
            ui.label("Netzwerkstatus:")
            charts.Charts.display_network_status_chart(network_status)