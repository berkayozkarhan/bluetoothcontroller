import components.conf as c
import dbus
import re


class BluezUtilError(Exception):
    pass


def byteArrayToHexString(bytes: bytes):
    hex_string = ""
    for byte in bytes:
        hex_byte = '%02X' % byte
        hex_string = hex_string + hex_byte

    return hex_string


def dbus_to_python(data):
    if isinstance(data, dbus.String):
        data = str(data)
    if isinstance(data, dbus.ObjectPath):
        data = str(data)
    elif isinstance(data, dbus.Boolean):
        data = bool(data)
    elif isinstance(data, dbus.Int64):
        data = int(data)
    elif isinstance(data, dbus.Int32):
        data = int(data)
    elif isinstance(data, dbus.Int16):
        data = int(data)
    elif isinstance(data, dbus.UInt16):
        data = int(data)
    elif isinstance(data, dbus.Byte):
        data = int(data)
    elif isinstance(data, dbus.Double):
        data = float(data)
    elif isinstance(data, dbus.Array):
        data = [dbus_to_python(value) for value in data]
    elif isinstance(data, dbus.Dictionary):
        new_data = dict()
        for key in data.keys():
            new_data[key] = dbus_to_python(data[key])
        data = new_data
    return data


def device_address_to_path(bdaddr: str, adapter_path: str):
    # e.g.convert 12:34:44:00:66:D5 on adapter hci0 to /org/bluez/hci0/dev_12_34_44_00_66_D5
    path = adapter_path + "/dev_" + bdaddr.replace(":", "_")
    return path


def path_to_device_address(path: str):
    # e.g. convert dev_12_34_56_78_9F_AB to 12:34:56:78:9F:AB
    last_part = path.split('/')[-1]
    # print("last_part = {}".format(last_part))
    return last_part[4:].replace('_', ':')


def get_name_from_uuid(uuid):
    if uuid in c.BluetoothConstants.UUID_NAMES:
        return c.BluetoothConstants.UUID_NAMES[uuid]
    else:
        return "Unknown"


def text_to_ascii_array(text):
    ascii_values = []
    for character in text:
        ascii_values.append(ord(character))
    return ascii_values


def print_properties(props):
    # dbus.Dictionary({dbus.String('SupportedInstances'): dbus.Byte(4, variant_level=1), dbus.String('ActiveInstances'): dbus.Byte(1, variant_level=1)}, signature=dbus.Signature('sv'))
    for key in props:
        print(key + "=" + str(props[key]))


def get_managed_objects():
    bus = dbus.SystemBus()
    obj = bus.get_object(c.BluetoothConstants.BLUEZ_SERVICE_NAME, '/')
    manager = dbus.Interface(obj, c.BluetoothConstants.DBUS_OM_IFACE)
    return manager.GetManagedObjects()


def find_adapter(pattern=None):
    return find_adapter_in_objects(get_managed_objects(), pattern)


def find_adapter_in_objects(objects, pattern=None):
    bus = dbus.SystemBus()

    for path, ifaces in objects.items():
        adapter = ifaces.get(c.BluetoothConstants.ADAPTER_INTERFACE)

        if adapter is None:
            continue

        if not pattern or pattern == adapter["Address"] or path.endswith(pattern):
            obj = bus.get_object(c.BluetoothConstants.BLUEZ_SERVICE_NAME, path)
            return dbus.Interface(obj, c.BluetoothConstants.ADAPTER_INTERFACE)

    raise BluezUtilError("Bluetooth adapter not found.")


def find_device(device_address, adapter_pattern=None):
    return find_device_in_objects(get_managed_objects(), device_address, adapter_pattern)


def find_device_in_objects(objects, device_address, adapter_pattern=None):
    bus = dbus.SystemBus()
    path_prefix = ""

    if adapter_pattern:
        print(f"Adapter pattern : {adapter_pattern}")
        adapter = find_adapter_in_objects(objects, adapter_pattern)
        path_prefix = adapter.object_path

    for path, ifaces in objects.items():
        device = ifaces.get(c.BluetoothConstants.DEVICE_INTERFACE)

        if device is None:
            continue

        if device["Address"] == device_address and path.startswith(path_prefix):
            obj = bus.get_object(c.BluetoothConstants.BLUEZ_SERVICE_NAME, path)
            return dbus.Interface(obj, c.BluetoothConstants.DEVICE_INTERFACE)

    # raise BluezUtilError("Bluetooth device not found.")
    return None


def get_found_devices():
    managed_objects = get_managed_objects()
    devices = {}
    for device_path in managed_objects:
        if '/org/bluez/hci0/dev_' in device_path:
            address_w_underscore = device_path.split('/org/bluez/hci0/dev_')[1]
            if len(address_w_underscore) > 17:
                continue
            device_address = path_to_device_address(device_path)
            devices[device_address] = managed_objects[device_path][c.BluetoothConstants.DEVICE_INTERFACE]
            devices[device_address].pop('Adapter', None)
            devices[device_address].pop('Modalias', None)

    return devices


def checkMAC(value):
    allowed = re.compile(r"""
                             (
                                 ^([0-9A-F]{2}[-]){5}([0-9A-F]{2})$
                                |^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$
                             )
                             """,
                         re.VERBOSE | re.IGNORECASE)

    if allowed.match(value) is None:
        return False
    else:
        return True


def remove_device(bd_addr: str):
    res = False
    try:
        bus = dbus.SystemBus()
        obj = bus.get_object(c.BluetoothConstants.BLUEZ_SERVICE_NAME, c.BluetoothConstants.ADAPTER_PATH)
        adapter_interface = dbus.Interface(obj, c.BluetoothConstants.ADAPTER_INTERFACE)
        device_path = device_address_to_path(bd_addr, c.BluetoothConstants.ADAPTER_PATH)
        adapter_interface.RemoveDevice(device_path)
        res = True
    except:
        res = False

    return res


def get_device_iface_by_path(device_path: str):
    """
        Get remote bluetooth device interface.
        param device_path : path of device ( e.g. : /org/bluez/hci0/dev_12_34_44_00_66_D5 )
        return : Device interface object(dbus.Interface) that contains the methods specified below.
            * CancelPairing
            * Connect
            * ConnectProfile
            * Disconnect
            * DisconnectProfile
            * Pair
    """
    bus = dbus.SystemBus()
    obj = bus.get_object(c.BluetoothConstants.BLUEZ_SERVICE_NAME, device_path)
    device = dbus.Interface(obj, c.BluetoothConstants.DEVICE_INTERFACE)
    return device


def get_adapter_props_iface():
    bus = dbus.SystemBus()
    adapter_object = bus.get_object(c.BluetoothConstants.BLUEZ_SERVICE_NAME, c.BluetoothConstants.ADAPTER_PATH)
    return dbus.Interface(adapter_object, c.BluetoothConstants.DBUS_PROPERTIES)


def get_bt_adapter():
    """
    Return : adapter_interface & props_iface as tuple (adapter_interface, props_iface)
    """
    adapter_interface = find_adapter()
    return adapter_interface


def get_device_properties_by_path(path):
    bus = dbus.SystemBus()
    obj = bus.get_object(c.BluetoothConstants.BLUEZ_SERVICE_NAME, path)
    props_iface = dbus.Interface(obj, c.BluetoothConstants.DBUS_PROPERTIES)
    device_properties = dbus_to_python(props_iface.GetAll(c.BluetoothConstants.DEVICE_INTERFACE))
    return device_properties


def get_device_properties_by_addr(bd_addr: str):
    bus = dbus.SystemBus()
    dev_path = device_address_to_path(bdaddr=bd_addr, adapter_path=c.BluetoothConstants.ADAPTER_PATH)
    obj = bus.get_object(c.BluetoothConstants.BLUEZ_SERVICE_NAME, dev_path)
    props_iface = dbus.Interface(obj, c.BluetoothConstants.DBUS_PROPERTIES)
    device_properties = dbus_to_python(props_iface.GetAll(c.BluetoothConstants.DEVICE_INTERFACE))
    return device_properties
