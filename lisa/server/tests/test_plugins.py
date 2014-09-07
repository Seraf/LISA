import os
from twisted.trial import unittest
from lisa.server.plugins.PluginManager import PluginManagerSingleton


class LisaPluginTestCase(unittest.TestCase):
    def setUp(self):
        self.pluginManager = PluginManagerSingleton.get()

    def test_a_install_plugin_ok(self):
        answer = self.pluginManager.installPlugin(plugin_name="UnitTest", test_mode=True, version='0.1.6')
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

    def test_d_upgrade_plugin_ok(self):
        answer = self.pluginManager.upgradePlugin(plugin_name="UnitTest", test_mode=True)
        self.assertEqual(answer['status'], "success")

    def test_dd_upgrade_plugin_fail(self):
        answer = self.pluginManager.upgradePlugin(plugin_name="UnitTest", test_mode=True)
        self.assertEqual(answer['status'], "fail")

    def test_e_load_plugin(self):
        answer = self.pluginManager.loadPlugins()
        test_list = ['UnitTest']
        self.assertListEqual(answer, test_list)

    def test_f_methodList_plugin(self):
        answer = self.pluginManager.methodListPlugin()
        methodlist = [{'methods': ['test'], 'plugin': u'UnitTest'}, {'core': 'intents', 'methods': ['list']}]
        self.assertListEqual(answer, methodlist)

    def test_g_create_plugin(self):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lisa.server.web.weblisa.settings")
        answer = self.pluginManager.createPlugin(plugin_name="TestPlugin", author_name="TestAuthor",
                                                 author_email="test@test.com")
        self.assertEqual(answer['status'], "success")

    def test_h_uninstall_plugin(self):
        answer = self.pluginManager.uninstallPlugin(plugin_name="UnitTest")
        self.assertEqual(answer['status'], "success")

    def test_hh_uninstall_plugin(self):
        answer = self.pluginManager.uninstallPlugin(plugin_name="UnitTest")
        self.assertEqual(answer['status'], "fail")