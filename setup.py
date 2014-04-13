from setuptools import setup, find_packages
from setuptools.command.install import install
import pip
import os
from django.core.management import call_command

# Ugly hack but django-tastypie-mongoengine require mongoengine 0.8.1
# but this version has some problem with new django versions
# As there's a bug with something I don't use, it doesn't matters
# if it use a newer version. So let's upgrade it programmatically
pip.main(['install', '-r', 'install/requirements.txt'])

VERSION = '0.1.0.15'

class LisaPluginInstaller(install):
    def run(self):
        install.run(self)
        # Make sure we refresh the plugin list when installing, so we know
        # we have enough write permissions.
        # see http://twistedmatrix.com/documents/current/core/howto/plugin.html
        # "when installing or removing software which provides Twisted plugins,
        # the site administrator should be sure the cache is regenerated"
        from twisted.plugin import IPlugin, getPlugins

        list(getPlugins(IPlugin))

if __name__ == '__main__':
    setup(
        cmdclass={'install': LisaPluginInstaller},
        version=VERSION,
        name='lisa-server',
        packages=find_packages() + ["twisted.plugins"],
        #package_data={'twisted.plugins': ['twisted/plugins/lisaserver_plugin.py']},
        url='http://www.lisa-project.net',
        license='MIT',
        author='Julien Syx',
        author_email='julien.syx@gmail.com',
        description='LISA home automation system - Server',
        include_package_data=True,
        namespace_packages=['lisa'],
        scripts = ['lisa/server/lisa-cli'],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lisa.server.web.weblisa.settings")
call_command('collectstatic', interactive=False)
