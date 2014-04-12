from setuptools import setup, find_packages
from pip.req import parse_requirements
import json
import pip
import os
from distutils.command.install_data import install_data
import shutil
from django.core.management import call_command

# Ugly hack but django-tastypie-mongoengine require mongoengine 0.8.1
# but this version has some problem with new django versions
# As there's a bug with something I don't use, it doesn't matters
# if it use a newer version. So let's upgrade it programmatically
pip.main(['install', '-r', 'install/requirements.txt'])

VERSION = '0.1.0.15'

"""
class my_install(install_data):
    def run(self):
        install_cmd = self.get_finalized_command('install')
        if install_cmd.root:
            self.install_dir = install_cmd.root
        else:
            self.install_dir = "/"
        install_data.run(self)
"""

if __name__ == '__main__':
    setup(
        #cmdclass={"install_data": my_install},
        version=VERSION,
        name='lisa-server',
        packages=find_packages() + [
        "twisted.plugins",
        ],
        #package_data={
        #    'twisted': ['plugins/lisaserver_plugin.py'],
        #},
        url='http://www.lisa-project.net',
        license='MIT',
        author='Julien Syx',
        author_email='julien.syx@gmail.com',
        description='LISA home automation system - Server',
        include_package_data=True,
        namespace_packages = ['lisa'],
        scripts = ['lisa/server/lisa-cli'],
        #data_files=[('etc/lisa/server/configuration', ['lisa/server/configuration/lisa.json.sample']),
        #            #('etc/init.d', ['lisa-server.init']),
        #            ],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
#            'Programming Language :: Python :: 3',
#            'Programming Language :: Python :: 3.4',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )

# Make Twisted regenerate the dropin.cache, if possible.  This is necessary
# because in a site-wide install, dropin.cache cannot be rewritten by
# normal users.
try:
    from twisted.plugin import IPlugin, getPlugins
except ImportError:
    pass
else:
    list(getPlugins(IPlugin))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lisa.server.web.weblisa.settings")
call_command('collectstatic', interactive=False)

# When pip installs anything from packages, py_modules, or ext_modules that
# includes a twistd plugin (which are installed to twisted/plugins/),
# setuptools/distribute writes a Package.egg-info/top_level.txt that includes
# "twisted".  If you later uninstall Package with `pip uninstall Package`,
# pip <1.2 removes all of twisted/ instead of just Package's twistd plugins.
# See https://github.com/pypa/pip/issues/355 (now fixed)
#
# To work around this problem, we monkeypatch
# setuptools.command.egg_info.write_toplevel_names to not write the line
# "twisted".  This fixes the behavior of `pip uninstall Package`.  Note that
# even with this workaround, `pip uninstall Package` still correctly uninstalls
# Package's twistd plugins from twisted/plugins/, since pip also uses
# Package.egg-info/installed-files.txt to determine what to uninstall,
# and the paths to the plugin files are indeed listed in installed-files.txt.
"""

try:
    from setuptools.command import egg_info
    egg_info.write_toplevel_names
except (ImportError, AttributeError):
    pass
else:
    def _top_level_package(name):
        return name.split('.', 1)[0]

    def _hacked_write_toplevel_names(cmd, basename, filename):
        pkgs = dict.fromkeys(
            [_top_level_package(k)
                for k in cmd.distribution.iter_distribution_names()
                if _top_level_package(k) != "twisted"
            ]
        )
        cmd.write_file("top-level names", filename, '\n'.join(pkgs) + '\n')

    egg_info.write_toplevel_names = _hacked_write_toplevel_names
"""

