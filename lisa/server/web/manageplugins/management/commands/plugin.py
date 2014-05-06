from django.core.management.base import BaseCommand, CommandError
from lisa.server.web.manageplugins.models import Plugin, Rule, Cron
from optparse import make_option
import os, json
import requests
from lisa.server.plugins.PluginManager import PluginManagerSingleton
from django.utils import six
import lisa.plugins
from lisa.server.web.weblisa.settings import configuration

class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()
        self.args = '<plugin_name>'
        self.help = 'Manage the plugins'

        self.plugins = []
        self.pluginPath = os.path.dirname(lisa.plugins.__file__) + '/'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.option_list = BaseCommand.option_list + (
            make_option('--list',
                action = 'store_true',
                help = 'List all plugins and show their status'),
            make_option('--create',
                action = 'store_true',
                help = 'Create a template plugin with a given name'),
            make_option('--enable',
                action = 'store_true',
                help = 'Enable a plugin'),
            make_option('--disable',
                action = 'store_true',
                help = 'Disable a plugin'),
            make_option('--install',
                action = 'store_true',
                help = 'Install a plugin'),
            make_option('--uninstall',
                action = 'store_true',
                help = 'Uninstall a plugin'),
            make_option('--upgrade',
                action = 'store_true',
                help = 'Upgrade a plugin'),
        )

    def handle(self, *args, **options):
        if args:
            self.arg_pluginName = args[0]

        if options.get('list'):
            self.plugin_list()
        elif options.get('install'):
            self.manage(name=self.arg_pluginName, action="install")
        elif options.get('uninstall'):
            self.manage(name=self.arg_pluginName, action="uninstall")
        elif options.get('enable'):
            self.manage(name=self.arg_pluginName, action="enable")
        elif options.get('disable'):
            self.manage(name=self.arg_pluginName, action="disable")
        elif options.get('create'):
            author_name = six.moves.input("What is your full name ? : ")
            print
            author_email = six.moves.input("What is your email ? : ")
            print
            self.manage(name=self.arg_pluginName, action="create", author_email=author_email, author_name=author_name)

    def get_pk(self, name):
        pluginDB = Plugin.objects(name=name)
        if pluginDB:
            return pluginDB['pk']

    def plugin_list(self):
        metareq = requests.get('/'.join([configuration['plugin_store'], 'plugins.json']))
        pluginDB = Plugin.objects()
        pluginlist_store = []
        pluginlist_local = []
        in_store = False
        if(metareq.ok):
            [pluginlist_store.append(item['name']) for item in json.loads(metareq.text or metareq.content)]
            [pluginlist_local.append(plugin['name']) for plugin in pluginDB]
            if pluginDB:
                for plugin in pluginDB:
                    for plugin_name in pluginlist_store:
                        if plugin['name'].lower() == plugin_name.lower():
                            self.plugins.append({"name": plugin['name'],
                                                 "installed": True,
                                                 "enabled": plugin['enabled']})
                            in_store = True
                    if not in_store:
                        self.plugins.append({"name": plugin['name'], "installed": True, "enabled": plugin['enabled']})
                    else:
                        in_store = False
            for plugin_store in pluginlist_store:
                if not plugin_store in pluginlist_local:
                    self.plugins.append({"name": plugin_store, "installed": False, "enabled": False})
        else:
            self.stdout.write(self.FAIL + "The plugin list seems to no be available" + self.ENDC)


        for pluginDict in self.plugins:
            if pluginDict['installed']:
                installed = "["+ self.OKGREEN + "Installed" + self.ENDC + "]"
            else:
                installed = "["+ self.FAIL + "Not installed" + self.ENDC + "]"
            if pluginDict['enabled']:
                enabled = "["+ self.OKGREEN + "Enabled" + self.ENDC + "]"
            else:
                enabled = "["+ self.FAIL + "Not enabled" + self.ENDC + "]"

            self.stdout.write("%s => %s %s" % (pluginDict['name'], installed, enabled))

    def manage(self, name, action, author_email=None, author_name=None):
        if action == "install":
            status = PluginManagerSingleton.get().installPlugin(plugin_name=name)
        elif action == "disable":
            status = PluginManagerSingleton.get().disablePlugin(plugin_name=name)
        elif action == "uninstall":
            status = PluginManagerSingleton.get().uninstallPlugin(plugin_name=name)
        elif action == "enable":
            status = PluginManagerSingleton.get().enablePlugin(plugin_name=name)
        elif action == "create":
            status = PluginManagerSingleton.get().createPlugin(plugin_name=name, author_name=author_name, author_email=author_email)
        else:
            exit()
        if status['status'] == 'success':
            self.stdout.write("[" + self.OKGREEN + "OK" + self.ENDC + "]" + " " + status['log'])
        else:
            self.stdout.write("[" + self.FAIL + "FAIL" + self.ENDC + "]" + " " + status['log'])