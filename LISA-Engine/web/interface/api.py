from tastypie import authorization
from tastypie import resources as tastyresources
from tastypie_mongoengine import resources as mongoresources
from interface.models import Workspace
from interface.models import WidgetUser, Widget
from tastypie_mongoengine import fields

try:
    from web.lisa.settings import LISA_PATH
except ImportError:
    from lisa.settings import LISA_PATH

class WidgetResource(mongoresources.MongoEngineResource):
    class Meta:
        queryset = Widget.objects.all()
        allowed_methods = ('get','post')
        authorization = authorization.Authorization()

class WidgetByUserResource(mongoresources.MongoEngineResource):
    class Meta:
        queryset = WidgetUser.objects.all()
        allowed_methods = ('get','post')
        authorization = authorization.Authorization()

    def obj_create(self, bundle, **kwargs):
        return super(WidgetByUserResource, self).obj_create(bundle, user=bundle.request.user)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

class WorkspaceResource(mongoresources.MongoEngineResource):
    class Meta:
        queryset = Workspace.objects.all()
        allowed_methods = ('get','post')
        authorization = authorization.Authorization()
