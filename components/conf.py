LOG_TYPE = 'c'
APP_NAME = 'bt-controller'


class BluetoothConstants:
    OBEX_BUS_NAME = 'org.bluez.obex'
    OBEX_PATH = '/org/bluez/obex'
    OBEX_AGENT_MANAGER_INTERFACE = 'org.bluez.obex.AgentManager1'
    OBEX_AGENT_INTERFACE = 'org.bluez.obex.Agent1'
    OBEX_TRANSFER_INTERFACE = 'org.bluez.obex.Transfer1'
    OBEX_SESSION_INTERFACE = 'org.bluez.obex.Session1'

    AGENT_PATH = "/amperino/bluetooth/agent"
    OBEX_AGENT_PATH = "/amperino/bluetooth/obex"
    AGENT_INTERFACE = 'org.bluez.Agent1'
    WATCH_RSSI = True
    MIN_ACCEPTABLE_VALUE_RSSI = -70

    BLUEZ_NAMESPACE = "/org/bluez/"
    BLUEZ_SERVICE_NAME = "org.bluez"

    ADAPTER_NAME = "hci0"
    ADAPTER_INTERFACE = BLUEZ_SERVICE_NAME + ".Adapter1"
    DEVICE_INTERFACE = BLUEZ_SERVICE_NAME + ".Device1"

    DBUS_PROPERTIES = "org.freedesktop.DBus.Properties"
    DBUS_OM_IFACE = "org.freedesktop.DBus.ObjectManager"
    DBUS_PROP_IFACE = "org.freedesktop.DBus.Properties"
    ADAPTER_PATH = BLUEZ_NAMESPACE + ADAPTER_NAME
    DEVICE_MAC_ADDRESS = "A4:93:3F:5B:3D:84"
    DEVICE_PATH = ADAPTER_PATH + "/dev_" + DEVICE_MAC_ADDRESS.replace(':', '_')

    GATT_MANAGER_INTERFACE = BLUEZ_SERVICE_NAME + ".GattManager1"
    GATT_SERVICE_INTERFACE = BLUEZ_SERVICE_NAME + ".GattService1"
    GATT_CHARACTERISTIC_INTERFACE = BLUEZ_SERVICE_NAME + ".GattCharacteristic1"
    GATT_DESCRIPTOR_INTERFACE = BLUEZ_SERVICE_NAME + ".GattDescriptor1"
    ADVERTISEMENT_INTERFACE = BLUEZ_SERVICE_NAME + ".LEAdvertisement1"
    ADVERTISING_MANAGER_INTERFACE = BLUEZ_SERVICE_NAME + ".LEAdvertisingManager1"

    UUID_NAMES = {
        "00001801-0000-1000-8000-00805f9b34fb": "Generic Attribute Service",
        "0000180a-0000-1000-8000-00805f9b34fb": "Device Information Service",
        "e95d93b0-251d-470a-a062-fa1922dfa9a8": "DFU Control Service",
        "e95d93af-251d-470a-a062-fa1922dfa9a8": "Event Service",
        "e95d9882-251d-470a-a062-fa1922dfa9a8": "Button Service",
        "e95d6100-251d-470a-a062-fa1922dfa9a8": "Temperature Service",
        "e95dd91d-251d-470a-a062-fa1922dfa9a8": "LED Service",
        "00002a05-0000-1000-8000-00805f9b34fb": "Service Changed",
        "e95d93b1-251d-470a-a062-fa1922dfa9a8": "DFU Control",
        "00002a05-0000-1000-8000-00805f9b34fb": "Service Changed",
        "00002a24-0000-1000-8000-00805f9b34fb": "Model Number String",
        "00002a25-0000-1000-8000-00805f9b34fb": "Serial Number String",
        "00002a26-0000-1000-8000-00805f9b34fb": "Firmware Revision String",
        "e95d9775-251d-470a-a062-fa1922dfa9a8": "micro:bit Event",
        "e95d5404-251d-470a-a062-fa1922dfa9a8": "Client Event",
        "e95d23c4-251d-470a-a062-fa1922dfa9a8": "Client Requirements",
        "e95db84c-251d-470a-a062-fa1922dfa9a8": "micro:bit Requirements",
        "e95dda90-251d-470a-a062-fa1922dfa9a8": "Button A State",
        "e95dda91-251d-470a-a062-fa1922dfa9a8": "Button B State",
        "e95d9250-251d-470a-a062-fa1922dfa9a8": "Temperature",
        "e95d93ee-251d-470a-a062-fa1922dfa9a8": "LED Text",
        "00002902-0000-1000-8000-00805f9b34fb": "Client Characteristic Configuration",
    }

    DEVICE_INF_SVC_UUID = "0000180a-0000-1000-8000-00805f9b34fb"
    MODEL_NUMBER_UUID = "00002a24-0000-1000-8000-00805f9b34fb"

    TEMPERATURE_SVC_UUID = "e95d6100-251d-470a-a062-fa1922dfa9a8"
    TEMPERATURE_CHR_UUID = "e95d9250-251d-470a-a062-fa1922dfa9a8"

    LED_SVC_UUID = "e95dd91d-251d-470a-a062-fa1922dfa9a8"
    LED_TEXT_CHR_UUID = "e95d93ee-251d-470a-a062-fa1922dfa9a8"

    SERVICE_UUID_MQTT = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    SERVICE_UUID_REST = "831d17be-bc93-45a0-8650-8f7d4923712a"


class BT_RESULT:
    OK = 1000

    ERR_UNAUTHORIZED_LOGIN = 1001
    ERR_KEY_NOT_FOUND = 1002
    ERR_MQTT_BROKER_CONNECTION = 1003


class MQTT:
    BROKER_HOST = 'localhost'
    BROKER_PORT = 1883

