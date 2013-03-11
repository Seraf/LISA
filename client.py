#!/usr/bin/env python
import sys
import pyjulius
import Queue

# Initialize and try to connect
client = pyjulius.Client('julius.julien-syx.fr', 10500)
try:
    client.connect()
except pyjulius.ConnectionError:
    print 'Start julius as module first!'
    sys.exit(1)

# Start listening to the server
client.start()
try:
    while 1:
        try:
            result = client.results.get(False)
        except Queue.Empty:
            continue
        print repr(result)
except KeyboardInterrupt:
    print 'Exiting...'
    client.stop()  # send the stop signal
    client.join()  # wait for the thread to die
    client.disconnect()  # disconnect from julius
