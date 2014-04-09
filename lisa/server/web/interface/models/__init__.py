try:
    from web.interface.models.widget import Widget, WidgetUser
    from web.interface.models.workspace import Workspace
except ImportError:
    from lisa.server.web.interface.models.widget import Widget, WidgetUser
    from lisa.server.web.interface.models.workspace import Workspace
