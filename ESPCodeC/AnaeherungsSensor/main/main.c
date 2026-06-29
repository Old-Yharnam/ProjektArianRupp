#include <stdbool.h>
#include <stdio.h>
#include "driver/gpio.h"
#include "esp_event.h"
#include "esp_log.h"
#include "esp_mac.h"
#include "esp_netif.h"
#include "esp_system.h"
#include "mqtt_client.h"
#include "nvs_flash.h"
#include "freertos/FreeRTOS.h"
#include "freertos/event_groups.h"
#include "freertos/task.h"
#include "esp_wifi.h"

#define SENSOR_GPIO_PIN GPIO_NUM_10
#define SENSOR_ACTIVE_LEVEL 0
#define SENSOR_POLL_DELAY_MS 10


#define WIFI_SSID "S25+ von Arian"
#define WIFI_PASSWORD "itnz2378igi8w2p"

#define MQTT_BROKER_HOST "10.43.132.71"
#define MQTT_BROKER_PORT 1883
#define MQTT_BROKER_USERNAME "mqtt_broker_aru7063"
#define MQTT_BROKER_PASSWORD "************"
#define MQTT_TOPIC "sensor/hw201/status"
#define MQTT_MESSAGE "Sensor hat ausgelöst"

static const char *TAG = "hw201_mqtt";
static EventGroupHandle_t wifi_event_group;
static esp_mqtt_client_handle_t mqtt_client;
static bool mqtt_connected;

enum {
	WIFI_CONNECTED_BIT = BIT0,
};

static void init_nvs(void)
{
	esp_err_t err = nvs_flash_init();
	if (err == ESP_ERR_NVS_NO_FREE_PAGES || err == ESP_ERR_NVS_NEW_VERSION_FOUND) {
		ESP_ERROR_CHECK(nvs_flash_erase());
		err = nvs_flash_init();
	}
	ESP_ERROR_CHECK(err);
}

static void publish_sensor_triggered(void)
{
	if (!mqtt_connected || mqtt_client == NULL) {
		ESP_LOGW(TAG, "MQTT nicht verbunden, Nachricht wird nicht gesendet");
		return;
	}

	int msg_id = esp_mqtt_client_publish(mqtt_client, MQTT_TOPIC, MQTT_MESSAGE, 0, 1, 0);
	ESP_LOGI(TAG, "MQTT Publish gesendet, msg_id=%d", msg_id);
}

static void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data)
{
	(void)handler_args;
	(void)base;
	esp_mqtt_event_handle_t event = event_data;

	switch ((esp_mqtt_event_id_t)event_id) {
		case MQTT_EVENT_CONNECTED:
			mqtt_connected = true;
			ESP_LOGI(TAG, "MQTT verbunden");
			break;
		case MQTT_EVENT_DISCONNECTED:
			mqtt_connected = false;
			ESP_LOGW(TAG, "MQTT getrennt");
			break;
		default:
			break;
	}
}

static void mqtt_start(void)
{
	esp_mqtt_client_config_t mqtt_cfg = {
		.broker.address.hostname = MQTT_BROKER_HOST,
		.broker.address.port = MQTT_BROKER_PORT,
		.broker.address.transport = MQTT_TRANSPORT_OVER_TCP,
		.credentials.username = MQTT_BROKER_USERNAME,
		.credentials.authentication.password = MQTT_BROKER_PASSWORD,
	};

	mqtt_client = esp_mqtt_client_init(&mqtt_cfg);
	ESP_ERROR_CHECK(esp_mqtt_client_register_event(mqtt_client, ESP_EVENT_ANY_ID, mqtt_event_handler, NULL));
	ESP_ERROR_CHECK(esp_mqtt_client_start(mqtt_client));
}

static void wifi_event_handler(void *arg, esp_event_base_t event_base, int32_t event_id, void *event_data)
{
	(void)arg;
	(void)event_data;

	if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START) {
		esp_wifi_connect();
		return;
	}

	if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
		mqtt_connected = false;
		xEventGroupClearBits(wifi_event_group, WIFI_CONNECTED_BIT);
		ESP_LOGW(TAG, "WLAN getrennt, neuer Verbindungsversuch");
		esp_wifi_connect();
		return;
	}

	if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
		xEventGroupSetBits(wifi_event_group, WIFI_CONNECTED_BIT);
		ESP_LOGI(TAG, "WLAN verbunden");
	}
}

static void wifi_init_sta(void)
{
	wifi_event_group = xEventGroupCreate();
	ESP_ERROR_CHECK(esp_netif_init());
	ESP_ERROR_CHECK(esp_event_loop_create_default());
	esp_netif_create_default_wifi_sta();

	wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
	ESP_ERROR_CHECK(esp_wifi_init(&cfg));

	ESP_ERROR_CHECK(esp_event_handler_register(WIFI_EVENT,
								 ESP_EVENT_ANY_ID,
								 &wifi_event_handler,
								 NULL));
	ESP_ERROR_CHECK(esp_event_handler_register(IP_EVENT,
								 IP_EVENT_STA_GOT_IP,
								 &wifi_event_handler,
								 NULL));

	wifi_config_t wifi_config = {
		.sta = {
			.threshold.authmode = WIFI_AUTH_WPA2_PSK,
		},
	};

	snprintf((char *)wifi_config.sta.ssid, sizeof(wifi_config.sta.ssid), "%s", WIFI_SSID);
	snprintf((char *)wifi_config.sta.password, sizeof(wifi_config.sta.password), "%s", WIFI_PASSWORD);

	ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
	ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config));
	ESP_ERROR_CHECK(esp_wifi_start());

	xEventGroupWaitBits(wifi_event_group,
						WIFI_CONNECTED_BIT,
						pdFALSE,
						pdTRUE,
						portMAX_DELAY);
}

static void sensor_gpio_init(void)
{
	gpio_config_t io_conf = {
		.pin_bit_mask = 1ULL << SENSOR_GPIO_PIN,
		.mode = GPIO_MODE_INPUT,
		.pull_up_en = GPIO_PULLUP_ENABLE,
		.pull_down_en = GPIO_PULLDOWN_DISABLE,
		.intr_type = GPIO_INTR_DISABLE,
	};

	ESP_ERROR_CHECK(gpio_config(&io_conf));
}

static bool sensor_is_triggered(void)
{
	return gpio_get_level(SENSOR_GPIO_PIN) == SENSOR_ACTIVE_LEVEL;
}

static void sensor_task(void *pvParameters)
{
	(void)pvParameters;
	bool last_trigger_state = sensor_is_triggered();

	while (true) {
		bool current_trigger_state = sensor_is_triggered();

		if (current_trigger_state && !last_trigger_state) {
			ESP_LOGI(TAG, "Sensor hat ausgelöst");
			publish_sensor_triggered();
		}

		last_trigger_state = current_trigger_state;
		vTaskDelay(pdMS_TO_TICKS(SENSOR_POLL_DELAY_MS));
	}
}

void app_main(void)
{
	init_nvs();
	wifi_init_sta();
	mqtt_start();
	sensor_gpio_init();

	xTaskCreate(sensor_task, "sensor_task", 4096, NULL, 5, NULL);
}
