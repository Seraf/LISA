+ quelle temperature fait il dans * ?
- <call>gettemperature <star></call>

+ quel température fait-il dans *
@ quelle temperature fait il dans * ?

> object gettemperature python
    import sys, os, inspect
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split( \
        inspect.getfile(inspect.currentframe()))[0],os.path.normpath("Plugins/Vera/lang/fr/modules/"))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

    from vera import Vera
    return Vera().getTemperature(args)
< object