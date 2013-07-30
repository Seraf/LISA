__author__ = 'juliensyx'
from django.conf import settings
from django.template.loader import BaseLoader
from django.template.base import Template, TemplateDoesNotExist

class Loader(BaseLoader):
    is_usable = True

    def load_template(self, template_name, template_dirs=None):
        source, origin = self.load_template_source(template_name, template_dirs)
        template = Template(source)
        return template, origin

    def load_template_source(self, template_name, template_dirs=None):
        try:
            with open(template_name, 'rb') as fp:
                return (fp.read().decode(settings.FILE_CHARSET), template_name)
        except IOError:
            raise TemplateDoesNotExist("Template does not exist")
