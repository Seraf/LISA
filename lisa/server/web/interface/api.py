from tastypie import authorization
from tastypie_mongoengine import resources as mongoresources
from lisa.server.web.interface.models import Workspace
from models import WidgetUser, Widget
from tastypie_mongoengine import fields

class WidgetResource(mongoresources.MongoEngineResource):
    plugin = fields.ReferenceField(to='lisa.server.web.manageplugins.api.PluginResource', attribute='plugin')

    class Meta:
        queryset = Widget.objects.all()
        allowed_methods = ('get','post')
        authorization = authorization.Authorization()

class WidgetByUserResource(mongoresources.MongoEngineResource):
    user = fields.ReferenceField(to='lisa.server.web.weblisa.api.UserResource', attribute='user')
    widget = fields.ReferenceField(to='lisa.server.web.interface.api.WidgetResource', attribute='widget', full=True)

    class Meta:
        queryset = WidgetUser.objects.all()
        allowed_methods = ('get','post','put','patch')
        authorization = authorization.Authorization()

    def obj_create(self, bundle, **kwargs):
        return super(WidgetByUserResource, self).obj_create(bundle, user=bundle.request.user)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

class WorkspaceResource(mongoresources.MongoEngineResource):
    user = fields.ReferenceField(to='lisa.server.web.weblisa.api.UserResource', attribute='user')
    widgets = fields.ReferencedListField(of='lisa.server.web.interface.api.WidgetByUserResource', attribute='widgets', full=True,
                                         null=True, help_text='List of widgets')

    class Meta:
        queryset = Workspace.objects.all()
        allowed_methods = ('get','post','put','patch')
        authorization = authorization.Authorization()
