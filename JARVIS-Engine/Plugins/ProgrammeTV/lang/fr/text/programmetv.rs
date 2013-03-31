+ <bot name> il y a quoi a la television ?
- <call>getprogrammetv</call>

> object getprogrammetv python
    import sys, os, inspect
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split( \
        inspect.getfile(inspect.currentframe()))[0],os.path.normpath("Plugins/ProgrammeTV/lang/fr/modules/"))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

    from programmetv import ProgrammeTV
    return ProgrammeTV().getProgrammeTV()
< object