import time

from components.bluetoothcontroller import Adapter
import unittest


class TestBluetoothAdapter(unittest.TestCase):
    def testSetDiscoverble(self):
        adapter = Adapter()
        discoverable = adapter.discoverable
        testDiscoverable = not discoverable

        adapter.set_discoverable(testDiscoverable)

        self.assertEqual(adapter.discoverable, testDiscoverable)

        # backup last state.
        adapter.set_discoverable(discoverable)

    def testSetPairable(self):
        adapter = Adapter()
        pairable = adapter.pairable
        testPairable = not pairable

        adapter.set_pairable(testPairable)

        self.assertEqual(adapter.pairable, testPairable)

        # backup last state.
        adapter.set_pairable(pairable)

    def testSetPowered(self):
        adapter = Adapter()
        powered = adapter.powered
        testPowered = not powered

        adapter.set_powered(testPowered)
        self.assertEqual(adapter.powered, testPowered)

        # backup last state.
        adapter.set_powered(powered)

    def testSetAlias(self):
        adapter = Adapter()
        alias = adapter.alias
        testAlias = "berkay"

        adapter.set_alias(testAlias)
        time.sleep(2)
        self.assertEqual(adapter.alias, testAlias)

        # backup last state.
        adapter.set_alias(alias)

    def testStartDiscovery(self):
        adapter = Adapter()

        self.assertEqual(adapter.start_discovery(), True)
        self.assertEqual(adapter.discovering, True)

        adapter.stop_discovery()

    def testStopDiscovery(self):
        adapter = Adapter()

        adapter.start_discovery()
        self.assertEqual(adapter.stop_discovery(), True)
        self.assertEqual(adapter.discovering, False)
