""" 
Modelierung des Netzwerkstatus, 
um die Informationen über die Verbindungsqualität und die Signalstärke zu speichern.
"""

class NetworkStatus:
    def __init__(self, signal_strength: int, connection_quality: str):
        self.signal_strength = signal_strength
        self.connection_quality = connection_quality

    def __str__(self):
        return f"NetworkStatus(signal_strength={self.signal_strength}, connection_quality='{self.connection_quality}')"