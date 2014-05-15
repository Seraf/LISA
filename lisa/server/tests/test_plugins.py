from lisa.server.plugins.PluginManager import PluginManagerSingleton
from twisted.trial import unittest

import json

class LisaPluginTestCase(unittest.TestCase):
    def setUp(self):
        self.pluginManager = PluginManagerSingleton.get()

    def test_a_install_plugin_ok(self):
        answer = self.pluginManager.installPlugin(plugin_name="UnitTest", test_mode=True)
        self.assertEqual(answer['status'], "success")

    def test_aa_install_plugin_fail(self):
        answer = self.pluginManager.installPlugin(plugin_name="UnitTest", test_mode=True)
        self.assertEqual(answer['status'], "fail")

    def test_b_disable_plugin_ok(self):
        answer = self.pluginManager.disablePlugin(plugin_name="UnitTest")
        self.assertEqual(answer['status'], "success")

    def test_bb_disable_plugin_fail(self):
        answer = self.pluginManager.disablePlugin(plugin_name="UnitTest")
        self.assertEqual(answer['status'], "fail")

    def test_c_enable_plugin_ok(self):
        answer = self.pluginManager.enablePlugin(plugin_name="UnitTest")
        self.assertEqual(answer['status'], "success")

    def test_cc_enable_plugin_fail(self):
        answer = self.pluginManager.enablePlugin(plugin_name="UnitTest")
        self.assertEqual(answer['status'], "fail")

    #def test_d_load_plugin(self):
    #    answer = self.pluginManager.loadPlugins()
    #    self.assertEqual(answer['status'], "fail")

    #def test_e_methodList_plugin(self):
    #    answer = self.pluginManager.methodListPlugin()
    #    self.assertEqual(answer['status'], "fail")

    def test_f_uninstall_plugin(self):
        answer = self.pluginManager.uninstallPlugin(plugin_name="UnitTest")
        self.assertEqual(answer['status'], "success")

    def test_ff_uninstall_plugin(self):
        answer = self.pluginManager.uninstallPlugin(plugin_name="UnitTest")
        self.assertEqual(answer['status'], "fail")

    def test_g_create_plugin(self):
        answer = self.pluginManager.createPlugin(plugin_name="TestPlugin", author_name="TestAuthor",
                                                 author_email="test@test.com")
        self.assertEqual(answer['status'], "fail")

