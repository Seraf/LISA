.. _lisa-wit:

LISA Wit
=============

Wit
-------
Wit is a Natural Language Processing tool.

This tool is used in L.I.S.A to parse the text sent by the client. Wit returns a structured JSON and this one is sent to the plugin (jsonInput parameter).

Wit installation
^^^^^^^^^^^^^^^^
At this moment Wit is not available in an offline mode. The Wit team announced that Wit will be gradually open sourced in the future, and an offline version is on the roadmap.

To use it online : https://www.wit.ai

Then, go to the bottom of the page and ask for an account saying you want to try wit with L.I.S.A

Developpers will give you an account, but during the waiting, read the documentation to see all possibilities and how it works.

Integration with plugins
^^^^^^^^^^^^^^^^^^^^^^^^
How your plugin's JSON should like: ::

    {
        "name": "ChatterBot",
        "version": "1.2.2",
        "author": "Julien Syx",
        "description": [
            {"lang": "fr", "description": "Ce plugin est celui par défaut intégrant les interactions basiques avec LISA"},
            {"lang": "en", "description": "This plugin is shipped by default, managing all basic interactions with LISA"},
            {"lang": "ru", "description": "Этот плагин по умолчанию интеграции основных взаимодействий с LISA"}
        ],
        "enabled": 1,
        "lang": ["fr","en","ru"],
        "configuration": {
            "intents": {
                "chatterbot_time": {
                    "method": "getTime",
                    "corpus": {}
                },
                "chatterbot_hello": {
                    "method": "sayHello",
                    "corpus": {}
                }
            },
            "widgets": {
                "getTime": "ChatterBot.web.views.widget1"
            }
        }
    }

On intents dictionary, you can create intent. By convention the format is <plugin>_<intent>.

Then in the method, you define the method name of your plugin class.
For example, the method getTime will call the method ChatterBot().getTime().

The method will automatically receive a json as argument containing all infos sent by Wit, and infos from sender.

Basically it contains the sentence spoken and a dictionary with this sentence processed (see Wit demo).

The corpus field will be removed in future version as developers of Wit want to do something similar to Github : the possibility to fork an intent.

Plugin's developers will be able to share their intents/entities and sentences associated, so it will be automatically added to your instance when you will install a plugin.
As an intent isn't shareable yet, please send me a mail at julien.syx@gmail.com and I will share you a screenshot of my intent to let you reproduce it for a plugin.