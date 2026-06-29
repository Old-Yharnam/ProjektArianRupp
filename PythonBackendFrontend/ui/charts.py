""" 
Diagramme und Datenvisualisierungen für die Benutzeroberfläche.
"""

from nicegui import ui

class Charts:
    @staticmethod
    def display_network_status_chart(network_status):
        with ui.card():
            ui.label("Netzwerkstatus")
            ui.echart({
                "xAxis": {"type": "category", "data": ["Signalstärke"]},
                "yAxis": {"type": "value"},
                "series": [{
                    "type": "bar",
                    "name": "dBm",
                    "data": [getattr(network_status, "signal_strength", 0)],
                    "itemStyle": {"color": "#4bc0c0"},
                }],
                "tooltip": {"trigger": "axis"},
            })