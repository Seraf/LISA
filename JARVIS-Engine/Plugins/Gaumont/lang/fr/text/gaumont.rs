+ il y a quoi au cinema
- <call>getfilms</call>

> object getfilms python
import sys, os, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split( \
    inspect.getfile(inspect.currentframe()))[0],os.path.normpath("Plugins/Gaumont/lang/fr/modules/"))))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from gaumont import Gaumont
return Gaumont().getFilms()
< object