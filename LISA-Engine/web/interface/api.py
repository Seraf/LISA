from tastypie import authorization
from tastypie import resources as tastyresources
from tastypie_mongoengine import resources as mongoresources
from interface.models import Workspace
from interface.models import WidgetUser, Widget
from tastypie_mongoengine import fields
from tastypie.utils import trailing_slash
from django.conf.urls.defaults import *
from twisted.python.reflect import namedAny

try:
    from web.lisa.settings import LISA_PATH
except ImportError:
    from lisa.settings import LISA_PATH

class WidgetResource(mongoresources.MongoEngineResource):
    plugin = fields.ReferenceField(to='web.plugins.api.PluginResource', attribute='plugin')

    class Meta:
        queryset = Widget.objects.all()
        allowed_methods = ('get','post')
        authorization = authorization.Authorization()

class WidgetByUserResource(mongoresources.MongoEngineResource):
    user = fields.ReferenceField(to='web.lisa.api.UserResource', attribute='user')
    widget = fields.ReferenceField(to='web.interface.api.WidgetResource', attribute='widget', full=True)

    class Meta:
        queryset = WidgetUser.objects.all()
        allowed_methods = ('get','post','put','patch')
        authorization = authorization.Authorization()
        extra_actions = [
            {
                'name': 'render_html',
                'summary': 'Return a widget html view',
                'http_method': 'GET',
                'fields':{
                    'x': {
                        'type': 'integer',
                        'required': True,
                        'description': 'The X coord'
                    },
                    'y': {
                        'type': 'integer',
                        'required': True,
                        'description': 'The Y coord'
                    }
                }
            }
            ]

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/render_html%s" % (self._meta.resource_name,
                trailing_slash()), self.wrap_view('render_html'), name="api_widget_render_html")
        ]

    def render_html(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        coord_x = request.GET.get("x")
        coord_y = request.GET.get("y")
        for widgetuser in WidgetUser.objects(pk=kwargs['pk']):
            widgetuser.coordx = coord_x
            widgetuser.coordy = coord_y
            widgetuser.save()
            widgetview = namedAny(widgetuser.widget.view)(request, coord_x, coord_y)
            self.log_throttled_access(request)
            return widgetview



    def obj_create(self, bundle, **kwargs):
        return super(WidgetByUserResource, self).obj_create(bundle, user=bundle.request.user)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

class WorkspaceResource(mongoresources.MongoEngineResource):
    user = fields.ReferenceField(to='web.lisa.api.UserResource', attribute='user')
    widgets = fields.ReferencedListField(of='web.interface.api.WidgetByUserResource', attribute='widgets', full=True,
                                         null=True, help_text='List of widgets')

    class Meta:
        queryset = Workspace.objects.all()
        allowed_methods = ('get','post','put','patch')
        authorization = authorization.Authorization()
