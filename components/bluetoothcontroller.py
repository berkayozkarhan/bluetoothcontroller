import dbus
import threading
import components.conf as c
import components.utils as u
from gi.repository import GObject
from dbus.mainloop.glib import DBusGMainLoop


class OperationModes:
    SCAN_ALL = 'scan-all'
    PAIR_TARGET = 'pair-target'


class BluetoothController(object):
    SUCCESSFUL = 1000
    UNDEFINED_MODE = 999

    def __init__(self):
        self.log_type = 'c'

        self.mode = None
        self._system_bus = None

        self._callback_mutex = threading.RLock()
        self.on_new_device_found = None

        self._target_bd_addr = None
        self._target_device_path = None
        self._target_bd_addr_set = None

        self._agent_mainloop = None
        self._service_mainloop = None
        self._scanner_mainloop = None
        self._timer_id = None

        self._scanner_thread = None
        self._agent_thread = None

        self._agent = None
        self._run_agent = False

        self._adapter_interface = None

        self._target_found = False
        self._connected_to_target = False
        self._paired_with_target = None
        self._trusted_device = False
        self._bt_is_discoverable = False

        self.__is_running = False

        self._devices = {}
        self.device_counter = 0
        self._discovering = False
        self._agent_registered = False

        self._callback_switcher = {
            'scan-all': {
                'on_start': self.start_scan_all,
                'new_device_found': self.new_device_found,
                'device_removed': self.device_removed,
                'device_properties_changed': self.device_properties_changed,
                'timeout': self.scan_all_timeout
            }
        }
        DBusGMainLoop(set_as_default=True)

    @property
    def on_new_device_found(self):
        return self._on_new_device_found

    @on_new_device_found.setter
    def on_new_device_found(self, callback):
        self._on_new_device_found = callback

    @staticmethod
    def log(msg, log_type):
        if 'c' in log_type:
            print("[BLUETOOTH CONTROLLER] " + msg)

    @staticmethod
    def get_device_properties_by_path(bus: dbus.SystemBus, path):
        obj = bus.get_object(c.BluetoothConstants.BLUEZ_SERVICE_NAME, path)
        props_iface = dbus.Interface(obj, c.BluetoothConstants.DBUS_PROPERTIES)
        device_properties = u.dbus_to_python(props_iface.GetAll(c.BluetoothConstants.DEVICE_INTERFACE))
        return device_properties

    def start(self, mode: str):
        """
        Start bluetooth discovery in specific mode
            :param mode : scan mode (check switcher variable)

            :return :
                    999 : Undefined mode
                    998 : Bluetooth already operating scan
                    997 : Discovery process still working
        """
        BluetoothController.log(msg=f"Running : {self.mode}", log_type=self.log_type)

        if self.__is_running:  # stop previous operation and remove resources left
            BluetoothController.log(msg=f"Running in operation mode : {self.mode}", log_type=self.log_type)
            BluetoothController.log(msg=f"Stopping operation mode : {self.mode}", log_type=self.log_type)
            self.stop()

        return self.start_discovery(mode)

    def stop(self):
        remove_resources = self._callback_switcher.get(self.mode).get('timeout')
        if remove_resources():  # check operation is successful or not
            BluetoothController.log(msg=f"Stopped operation mode : {self.mode}", log_type=self.log_type)
        else:
            BluetoothController.log(msg="Error while removing resources.", log_type=self.log_type)

    def start_discovery(self, mode: str):
        if mode not in self._callback_switcher:
            BluetoothController.log(msg=f"Undefined mode : {mode}", log_type=self.log_type)
            return self.UNDEFINED_MODE

        self.mode = mode
        start_mode_operation = self._callback_switcher.get(self.mode).get('on_start')
        if start_mode_operation():
            BluetoothController.log(msg=f"Started in mode : {self.mode}", log_type=self.log_type)

    def start_scan_all(self):
        """
        Scan nearby devices for 30 seconds.
        return : True-False
        """
        self._system_bus = dbus.SystemBus()
        self._scanner_mainloop = GObject.MainLoop()
        self._scanner_thread = threading.Thread(target=self._scanner_mainloop.run)

        adapter_path = c.BluetoothConstants.BLUEZ_NAMESPACE + c.BluetoothConstants.ADAPTER_NAME
        adapter_object = self._system_bus.get_object(c.BluetoothConstants.BLUEZ_SERVICE_NAME, adapter_path)
        self._adapter_interface = dbus.Interface(adapter_object, c.BluetoothConstants.ADAPTER_INTERFACE)

        mode_callbacks = self._callback_switcher.get(self.mode)

        self._system_bus.add_signal_receiver(mode_callbacks['new_device_found'],
                                             dbus_interface=c.BluetoothConstants.DBUS_OM_IFACE,
                                             signal_name="InterfacesAdded")

        self._system_bus.add_signal_receiver(mode_callbacks['device_removed'],
                                             dbus_interface=c.BluetoothConstants.DBUS_OM_IFACE,
                                             signal_name="InterfacesRemoved")
        self._system_bus.add_signal_receiver(mode_callbacks['device_properties_changed'],
                                             dbus_interface=c.BluetoothConstants.DBUS_PROPERTIES,
                                             signal_name="PropertiesChanged", path_keyword="path")

        self._timer_id = GObject.timeout_add(30 * 1000, mode_callbacks['timeout'])
        self._adapter_interface.StartDiscovery()

        BluetoothController.log(msg="Discovery started.", log_type=self.log_type)
        self._scanner_thread.start()

    def new_device_found(self, path, interfaces):
        """
        Handler function for handle 'InterfacesAdded' signal
        """
        if c.BluetoothConstants.DEVICE_INTERFACE not in interfaces:
            return
        device_properties = BluetoothController.get_device_properties_by_path(self._system_bus, path)

        # for prop in device_properties:
            # BluetoothController.log(msg=f"[NEW] {prop} : {device_properties[prop]}", log_type=self.log_type)

        self.device_counter += 1

        if self._on_new_device_found is not None:
            self._on_new_device_found(device_properties)

        # BluetoothController.log(msg="-" * 30, log_type=self.log_type)

    def device_removed(self, path, interfaces):
        """
        Handler function for InterfacesRemoved signal
        """
        # interfaces is an array of dictionary string in this signal
        if c.BluetoothConstants.DEVICE_INTERFACE not in interfaces:
            return
        if path in self._devices:
            dev = self._devices[path]
            if 'Address' in dev:
                BluetoothController.log(msg=f"[DEL] BDADDR : {dev['Address']}", log_type=self.log_type)
            else:
                BluetoothController.log(msg=f"[DEL] PATH : {path}", log_type=self.log_type)
            BluetoothController.log(msg="-" * 30, log_type=self.log_type)
            self.device_counter -= 1
            del self._devices[path]

    def device_properties_changed(self, interface, changed, invalidated, path):
        """
        Handler function to monitor device's changing characteristics
        """
        if interface != c.BluetoothConstants.DEVICE_INTERFACE:
            return
        if path in self._devices:
            self._devices[path] = dict(self._devices[path].items())
            self._devices[path].update(changed.items())
        else:
            self._devices[path] = changed
            # self._new_devices_counter += 1

        dev = self._devices[path]
        BluetoothController.log(msg=f"[CHG] PATH : {path}", log_type=self.log_type)

        if 'Address' in dev:
            BluetoothController.log(msg=f"[CHG] BDADDR : {dev['Address']}", log_type=self.log_type)
        if 'Name' in dev:
            BluetoothController.log(msg=f"[CHG] NAME : {dev['Name']}", log_type=self.log_type)
        if 'RSSI' in dev:
            BluetoothController.log(msg=f"[CHG] RSSI : {dev['RSSI']}", log_type=self.log_type)

        device_address = u.path_to_device_address(path)

        BluetoothController.log(msg="-" * 30, log_type=self.log_type)

    def scan_all_timeout(self):
        if self._timer_id is not None:
            GObject.source_remove(self._timer_id)
        if self._scanner_mainloop is not None:
            self._scanner_mainloop.quit()

        if self._adapter_interface is not None:
            try:
                self._adapter_interface.StopDiscovery()
            except Exception as e:
                BluetoothController.log(msg=f"Error while stopping discovery : {e.args}", log_type=self.log_type)

        self._system_bus.remove_signal_receiver(self.new_device_found, "InterfacesAdded")
        self._system_bus.remove_signal_receiver(self.device_removed, "InterfacesRemoved")
        self._system_bus.remove_signal_receiver(self.device_properties_changed, "PropertiesChanged")

        self._timer_id = None
        self._adapter_interface = None

        self._discovering = False

        BluetoothController.log(msg="Discovery timeout.", log_type=self.log_type)
        BluetoothController.log(msg=f"Discovering : {self._discovering}", log_type=self.log_type)

        BluetoothController.log(msg=f"{self.device_counter} devices found.", log_type=self.log_type)

        self.device_counter = 0
        self.__is_running = False
        self._discovering = False

        BluetoothController.log(msg=f"Stopped operation : {self.mode}", log_type=self.log_type)
        BluetoothController.log(msg="Summary : ", log_type=self.log_type)
        self.show_controller_info()

        self._scanner_mainloop = None
        self._scanner_thread = None

    def show_controller_info(self):
        BluetoothController.log(msg="#" * 15, log_type=self.log_type)
        for prop in self.__dict__:
            BluetoothController.log(msg=f"{prop} : {self.__dict__[prop]}", log_type=self.log_type)
        BluetoothController.log(msg="#" * 15, log_type=self.log_type)


