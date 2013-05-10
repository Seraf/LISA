+ qui *
- <call>ask_izipedia <star></call>

+ où *
- <call>ask_izipedia <star></call>

+ ou *
- <call>ask_izipedia <star></call>

+ quoi *
- <call>ask_izipedia <star></call>

+ comment *
- <call>ask_izipedia <star></call>

+ quand *
- <call>ask_izipedia <star></call>

+ quelle *
- <call>ask_izipedia <star></call>

+ quel *
- <call>ask_izipedia <star></call>

> object ask_izipedia python
import sys, os, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split( \
    inspect.getfile(inspect.currentframe()))[0],os.path.normpath("Plugins/Izipedia/lang/fr/modules/"))))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from izipedia import Izipedia
return Izipedia().ask_izipedia(args)
< object
