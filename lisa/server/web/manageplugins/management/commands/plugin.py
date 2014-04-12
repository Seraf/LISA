from django.core.management.base import BaseCommand, CommandError
from lisa.server.web.manageplugins.models import Plugin, Rule, Cron
from optparse import make_option
import os, json
import requests
from lisa.server.web.manageplugins.functions import install, uninstall, enable, disable, create
from django.utils import six
from lisa.server.web.weblisa.settings import LISA_PATH, configuration

class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()
        self.args = '<plugin_name>'
        self.help = 'Manage the plugins'

        self.plugins = []
        self.pluginPath = configuration['plugin_path'] + '/'
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
        pluginLocalList = os.listdir(self.pluginPath)
        metareq = requests.get('https://raw.github.com/Seraf/LISA-Plugins/master/plugin_list.json')
        if(metareq.ok):
            for item in json.loads(metareq.text or metareq.content):
                pluginDB = Plugin.objects(name=item['name'])
                if pluginDB:
                    for plugin in pluginDB:
                        self.plugins.append({"name": item['name'], "installed": True, "enabled": plugin['enabled']})
                        if item['name'] in pluginLocalList:
                            pluginLocalList.remove(item['name'])
                else:
                    self.plugins.append({"name": item['name'], "installed": False, "enabled": False})
                    if item['name'] in pluginLocalList:
                        pluginLocalList.remove(item['name'])
        else:
            self.stdout.write(self.FAIL + "The plugin list on github seems to no be available" + self.ENDC)
        for pluginName in pluginLocalList:
            if os.path.isdir(os.path.join(self.pluginPath, pluginName)):
                pluginDB = Plugin.objects(name=pluginName)
                if pluginDB:
                    for plugin in pluginDB:
                        self.plugins.append({"name": plugin['name'], "installed": True, "enabled": plugin['enabled']})
                        if plugin['name'] in pluginLocalList:
                            pluginLocalList.remove(plugin['name'])
                else:
                    self.plugins.append({"name": pluginName, "installed": False, "enabled": False})
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
            plugin_url = None
            plugin_sha = None
            metareq = requests.get('https://raw.github.com/Seraf/LISA-Plugins/master/plugin_list.json')
            if(metareq.ok):
                for item in json.loads(metareq.text or metareq.content):
                    if item['name'] == name:
                        plugin_url, plugin_sha = item['url'], item['sha']
            else:
                self.stdout.write(self.FAIL + "The plugin list on github seems to no be available" + self.ENDC)

            status = install(plugin_sha=plugin_sha, plugin_url=plugin_url, plugin_name=name)
        elif action == "disable":
            status = disable(plugin_name=name)
        elif action == "uninstall":
            status = uninstall(plugin_name=name)
        elif action == "enable":
            status = enable(plugin_name=name)
        elif action == "create":
            status = create(plugin_name=name, author_name=author_name, author_email=author_email)
        else:
            exit()
        if status['status'] == 'success':
            self.stdout.write("[" + self.OKGREEN + "OK" + self.ENDC + "]" + " " + status['log'])
        else:
            self.stdout.write("[" + self.FAIL + "FAIL" + self.ENDC + "]" + " " + status['log'])