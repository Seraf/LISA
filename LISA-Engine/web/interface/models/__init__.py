try:
    from web.interface.models.widget import Widget, WidgetUser
    from web.interface.models.workspace import Workspace
except ImportError:
    from interface.models.widget import Widget, WidgetUser
    from interface.models.workspace import Workspace
