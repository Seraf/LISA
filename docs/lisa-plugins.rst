.. _lisa-engine:

LISA Plugins
=============

Plugins
-------
All plugins have the same structure: ::

    .
    ├── chatterbot.json
    ├── lang
    │   ├── en
    │   │   ├── chat.rs
    │   │   └── LC_MESSAGES
    │   │       ├── chat.mo
    │   │       └── chat.po
    │   ├── fr
    │   │   ├── chat.rs
    │   │   └── LC_MESSAGES
    │   │       ├── chat.mo
    │   │       └── chat.po
    │   └── ru
    │       ├── chat.rs
    │       └── LC_MESSAGES
    │           ├── chat.mo
    │           └── chat.po
    ├── modules
    │   └── chat.py
    ├── README.rst
    ├── tests
    │   └── chat_test.py
    └── web
        ├── api.py
        ├── __init__.py
        ├── models.py
        ├── templates
        │   └── widget.html
        ├── tests.py
        ├── urls.py
        └── views.py


- A README file to explain what the plugin do and how it works
- A json file used for setup of the plugin, containing cron, rules, and parameters to setup (used only for the install)
- A lang directory containing all langs available
- A text file (.rs) containing all sentences and rules to launch a function
- A module file (.py) containing the class and all the methods called by text file
- The web directory allow to expose the plugin in the L.I.S.A API and can be used to add widgets on L.I.S.A dashboard
Language file
^^^^^^^^^^^^^
The module is generic and should use gettext. The id of the string should be in english.
To add a new translation, add a LC_MESSAGE directory, then (replace <domain> by the name of your plugin : ::

    xgettext --language=Python --keyword=_ --output=<domain>.po --from-code=UTF-8 `find . -name "*.py"`

This will generate a translation source file. To be used, you need to compile it (each time you will do a modification) : ::

    msgfmt <domain>.po --output-file <domain>.mo

Text file
^^^^^^^^^
The text file is in a Rivescript format. You will get more information about this "language" on
http://www.rivescript.com .

Example: ::

    + give me the tv guide [*]
    - <call>getprogrammetv</call>

    > object getprogrammetv python
        import sys, os, inspect
        cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split( \
            inspect.getfile(inspect.currentframe()))[0],os.path.normpath("Plugins/ProgrammeTV/modules/"))))
        if cmd_subfolder not in sys.path:
            sys.path.insert(0, cmd_subfolder)

        from programmetv import ProgrammeTV
        return ProgrammeTV().getProgrammeTV()
    < object

Module file
^^^^^^^^^^^
Example of plugin : ::

    # -*- coding: UTF-8 -*-
    import urllib, json
    import xml.etree.ElementTree as ET
    from datetime import date
    import os
    from pymongo import MongoClient

    import gettext

    path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
    inspect.getfile(inspect.currentframe()))[0],os.path.normpath("../lang/"))))
    _ = translation = gettext.translation(domain='programmetv', localedir=path, languages=[configuration['lang']]).ugettext

    class ProgrammeTV:
        def __init__(self):
            self.configuration_lisa = json.load(open('Configuration/lisa.json'))
            mongo = MongoClient(self.configuration_lisa['database']['server'],
                                self.configuration_lisa['database']['port'])
            self.configuration = mongo.lisa.plugins.find_one({"name": "ProgrammeTV"})

        def getProgrammeTV(self):
            programmetv_str = [...] <<< Here the code to fill a string and return it as an answer
            return json.dumps({"plugin": "programmetv","method": "getProgrammeTV", "body": programmetv_str})

There's many possibilities, code is flexible and there's no limit except one : you have to always return a JSON.

The JSON must contain the plugin name, the method called, and the answer in the "body" field.

You can also return any extra data in the field name of your choice. It can be used by the rule engine to match
some condition and/or feed other plugins with these data.

Unit tests
^^^^^^^^^^
Each plugin should come with unit tests. It allows to be sure everything is OK and there's nothing broken from an old
version to a newer. To have your plugin registered on the github repository, your plugin must provide unit tests and
they should be OK.

Unit test use the LISA-Engine to test if the sentence provided return the good answer.

Example of a unit test : ::

    import json, os, sys
    from twisted.trial import unittest
    from twisted.test import proto_helpers
    sys.path.append(os.path.normpath(os.path.join(os.path.abspath("../../../"))))
    import libs
    from lisa import configuration

    class ChatTestCase(unittest.TestCase):
        def setUp(self):
            factory = libs.LisaInstance
            self.proto = factory.buildProtocol(('127.0.0.1', 0))
            self.tr = proto_helpers.StringTransport()
            self.proto.makeConnection(self.tr)


        # Build simulate data received (json data)
        def _test(self, sentence, expected):
            self.proto.dataReceived(json.dumps({"type": "Chat", "zone": "Test",
                                                "from": "Test",
                                                "body": '%s' % (sentence)
            }))
            jsonAnswer = json.loads(self.tr.value())
            # We check if the answer is equal to what we expected
            self.assertEqual(jsonAnswer['body'], expected)

        # Inject some sentences to test depending the language used
        def test_hello(self):
            if configuration['lang'] == 'en':
                return self._test(sentence='chat test', expected='chat OK')
            elif configuration['lang'] == 'fr':
                return self._test(sentence='Bonjour', expected='Bonjour. Comment allez vous ?')
