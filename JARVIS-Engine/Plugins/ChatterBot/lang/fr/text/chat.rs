! var name = jarvis
! global debug = true

+ il est quelle heure[*]
- <call>gettime</call>

+ il est quel heure[*]
@ il est quelle heure[*]

+ *
- Je ne suis pas sur de bien vous comprendre.
- Continuez.
- Intéressant. Je vous pris de continuer.
- Dites m'en plus.
- Est ce qu'en parler vous ennuie ?

+ [*] (désolé|excuse|excuses) [*]
- Ne vous excusez pas pour ça.
- Vos excuses ne sont pas nécessaires.
- Je vous ai déjà dit qu'il ne fallait pas vous excuser.
- Ca ne me dérange pas. Continuez.

+ je me souviens *
- Vous pensez souvent à <star>?
- Est ce que penser à <star> vous fait penser à quelque chose d'autre?

+ (salut|hello|bonjour|hi|hey|howdy|hola|hai|yo) [*]
- Bonjour. Comment allez vous ?

+ [*] (fuck|fucker|shit|damn|shut up|bitch|encule|connard|con) [*]
- Ca y'est? Vous vous sentez mieux?
- Vous êtes enervé je suppose?

> object gettime python
import sys, os, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split( \
    inspect.getfile(inspect.currentframe()))[0],os.path.normpath("Plugins/ChatterBot/lang/fr/modules/"))))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from chat import Chat
return Chat().getTime()
< object