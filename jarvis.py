import os
import sys
import fnmatch
import pyjulius
import libs


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

#Loading Julius
try:
    # Initialize and try to connect
    global client
    client = pyjulius.Client('localhost', 10500)
    client.connect()
except pyjulius.ConnectionError:
    print 'Julius is not started as a module'


def main():
    # Load and teach the bot
    if exists('bot_library'):
        for root, dirnames, filenames in os.walk('Plugins'):
            for filename in fnmatch.filter(filenames, '*.rs'):
                bot_library.learn(root)

    print "Starting to poll for messages..."

    """
    # Start listening to the server (audio part)
    client.start()
    try:
        while 1:
            try:
                result = client.results.get(False)
                # Should analyze here
            except Queue.Empty:
                continue
            print repr(result)
    except KeyboardInterrupt:
        print 'Exiting...'
        client.stop()  # send the stop signal
        client.join()  # wait for the thread to die
        client.disconnect()  # disconnect from julius
    """
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
