+ events * ?
- <call>getcalendars <star></call>

> object getcalendars python
    import sys, os, inspect
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split( \
        inspect.getfile(inspect.currentframe()))[0],os.path.normpath("Plugins/Google/lang/fr/modules/"))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

    from google import Google
    return Google().getCalendars(args)
< object