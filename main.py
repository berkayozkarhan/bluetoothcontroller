from components.bluetoothcontroller import BluetoothController, OperationModes


def on_new_device_found(device_props):
    for prop in device_props:
        print(f"[CHG] {prop} : {device_props[prop]}")


if __name__ == '__main__':
    bt = BluetoothController()
    bt.on_new_device_found = on_new_device_found
    bt.start(OperationModes.SCAN_ALL)
    print("tt")
