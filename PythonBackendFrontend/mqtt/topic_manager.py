""" 
Verwltet und sammelt die MQTT-Topics, die von den Clients abonniert werden.
Dadurch muss nur diese Datei angepasst werden, wenn sich die Topics ändern, und nicht die gesamte Logik in den Clients.
"""

import config.settings as settings

class MQTTTopicManager:
    def __init__(self):
        self.topics = {
            "ESP-Sensor": settings.MQTT_TOPIC_COMMANDS,
        }

    def get_topic(self, topic_name):
        return self.topics.get(topic_name, None)