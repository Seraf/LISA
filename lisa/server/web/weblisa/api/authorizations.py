import logging
 
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import Unauthorized
 
 
logger = logging.getLogger(__name__)
 
 
class UserOnlyAuthorization(DjangoAuthorization):
 
    """
        Authorization class for User objects.
    """
 
    def generic_base_check(self, object_list, bundle):
        """
            Returns False if either:
                a) if the `object_list.model` doesn't have a `_meta` attribute
                b) the `bundle.request` object doesn have a `user` attribute
        """
        klass = self.base_checks(bundle.request, object_list.model)
        if klass is False:
            raise Unauthorized("You are not allowed to access that resource.")
        return True
 
    def generic_item_check(self, object_list, bundle):
        if not self.generic_base_check(object_list, bundle):
            raise Unauthorized("You are not allowed to access that resource.")
        path_list = [(p) for p in bundle.request.path.split('/') if len(p)]
        if path_list[-1] == "schema":
            return True
        if not bundle.request.user == bundle.obj:
            raise Unauthorized("You are not allowed to access that resource.")
 
        return True
 
    def generic_list_check(self, object_list, bundle):
        if not self.generic_base_check(object_list, bundle):
            raise Unauthorized("You are not allowed to access that resource.")
 
        return object_list.filter(pk=bundle.request.user.id)
 
    # List Checks
    def create_list(self, object_list, bundle):
        return self.generic_list_check(object_list, bundle)
 
    def read_list(self, object_list, bundle):
        return self.generic_list_check(object_list, bundle)
 
    def update_list(self, object_list, bundle):
        return self.generic_list_check(object_list, bundle)
 
    def delete_list(self, object_list, bundle):
        return self.generic_list_check(object_list, bundle)
 
    # Item Checks
    def create_detail(self, object_list, bundle):
        return self.generic_item_check(object_list, bundle)
 
    def read_detail(self, object_list, bundle):
        return self.generic_item_check(object_list, bundle)
 
    def update_detail(self, object_list, bundle):
        return self.generic_item_check(object_list, bundle)
 
    def delete_detail(self, object_list, bundle):
        return self.generic_item_check(object_list, bundle)