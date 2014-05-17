from twisted.python import log
import os
import pkg_resources
import json

class ConfigManager(object):
    """
    """

    def __init__(self):
        self.configuration = {}
        if not os.path.exists('/etc/lisa/server/lisa.json'):
            self.configuration = json.load(open(pkg_resources.resource_filename(__name__, 'configuration/lisa.json.sample')))
        else:
            self.configuration = json.load(open('/etc/lisa/server/lisa.json'))

        self.dir_path = os.path.dirname(__file__)

    def getConfiguration(self):
        return self.configuration

    def setConfiguration(self, path):
        if os.path.exists(path) and path.endswith('.json'):
            self.configuration = json.load(open(path))

    def getPath(self):
        return self.dir_path



class ConfigManagerSingleton(object):
    """
    Singleton version of the config manager.

    Being a singleton, this class should not be initialised explicitly
    and the ``get`` classmethod must be called instead.

    To call one of this class's methods you have to use the ``get``
    method in the following way:
    ``ConfigManagerSingleton.get().themethodname(theargs)``
    """

    __instance = None

    def __init__(self):
        """
        Initialisation: this class should not be initialised
        explicitly and the ``get`` classmethod must be called instead.
        """

        if self.__instance is not None:
            raise Exception("Singleton can't be created twice !")

    def get(self):
        """
        Actually create an instance
        """
        if self.__instance is None:
            self.__instance = ConfigManager()
            log.msg("ConfigManagerSingleton initialised")
        return self.__instance
    get = classmethod(get)