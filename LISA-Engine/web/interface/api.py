from tastypie import authorization
from tastypie import resources
from interface.models import Workspace
from interface.models import WidgetUser

try:
    from web.lisa.settings import LISA_PATH
except ImportError:
    from lisa.settings import LISA_PATH

class WidgetResource(resources.MongoEngineResource):
    class Meta:
        queryset = WidgetUser.objects.all()
        allowed_methods = ('get','post')
        authorization = authorization.Authorization()

class WorkspaceResource(resources.MongoEngineResource):
    class Meta:
        queryset = Workspace.objects.all()
        allowed_methods = ('get','post')
        authorization = authorization.Authorization()
