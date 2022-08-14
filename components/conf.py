LOG_TYPE = 'c'
APP_NAME = 'bt-controller'


class BluetoothConstants:
    OBEX_BUS_NAME = 'org.bluez.obex'
    OBEX_PATH = '/org/bluez/obex'
    OBEX_AGENT_MANAGER_INTERFACE = 'org.bluez.obex.AgentManager1'
    OBEX_AGENT_INTERFACE = 'org.bluez.obex.Agent1'
    OBEX_TRANSFER_INTERFACE = 'org.bluez.obex.Transfer1'
    OBEX_SESSION_INTERFACE = 'org.bluez.obex.Session1'

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
