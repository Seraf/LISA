import os
import sys
import fnmatch
import libs
import xml.etree.ElementTree as ET

def exists(x):
    if x in globals():
        return True
    else:
        return False

#Loading Jarvis
try:
    global bot_library
    bot_library = libs.RiveScriptBot()
    print "Successfully loaded bot"
except:
    print "Couldn't load bot"


def main():
    # Load and teach the bot
    if exists('bot_library'):
        for root, dirnames, filenames in os.walk('Plugins'):
            for filename in fnmatch.filter(filenames, '*.rs'):
                configuration = ET.parse('Plugins/Configuration/jarvis.xml').getroot()
                if 'lang/'+configuration.findtext('lang') in root or filename=='begin.rs':
                    bot_library.learn(root)

    print "Starting to poll for messages..."

    # For tests only, listen on the stdin
    while True:
        line = sys.stdin.readline()
        if exists('bot_library'):
            response = bot_library.respond_to(str(line))
            print response
        else:
            print "There is no bot to provide a response"

if __name__ == '__main__':
    main()
