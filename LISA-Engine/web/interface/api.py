from tastypie import authorization
from tastypie import resources as tastyresources
from tastypie_mongoengine import resources as mongoresources
from interface.models import Workspace
from interface.models import WidgetUser

try:
    from web.lisa.settings import LISA_PATH
except ImportError:
    from lisa.settings import LISA_PATH

class WidgetResource(mongoresources.MongoEngineResource):
    class Meta:
        queryset = WidgetUser.objects.all()
        allowed_methods = ('get','post')
        authorization = authorization.Authorization()

class WorkspaceResource(mongoresources.MongoEngineResource):
    class Meta:
        queryset = Workspace.objects.all()
        allowed_methods = ('get','post')
        authorization = authorization.Authorization()
