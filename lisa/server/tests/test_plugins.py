from lisa.server.plugins.PluginManager import PluginManagerSingleton
from twisted.trial import unittest

import json

class LisaClientTestCase_Plugin(unittest.TestCase):
    def setUp(self):
        self.pluginManager = PluginManagerSingleton.get()

    def test_a_install_plugin(self):
        answer = self.pluginManager.installPlugin(plugin_name="UnitTest", test_mode=True)
        self.assertEqual(answer['status'], "success")

    def test_b_disable_plugin(self):
        answer = self.pluginManager.disablePlugin(plugin_name="UnitTest")
        self.assertEqual(answer['status'], "success")

    def test_c_enable_plugin(self):
        answer = self.pluginManager.enablePlugin(plugin_name="UnitTest")
        self.assertEqual(answer['status'], "success")

    def test_d_uninstall_plugin(self):
        answer = self.pluginManager.uninstallPlugin(plugin_name="UnitTest")
        self.assertEqual(answer['status'], "success")
