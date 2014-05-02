from setuptools import setup
import os
from django.core.management import call_command

VERSION = '0.1.1.33'

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

def listify(filename):
    return filter(None, open(filename, 'r').read().strip('\n').split('\n'))

if __name__ == '__main__':
    setup(
        version=VERSION,
        name='lisa-server',
        packages=["lisa", "twisted.plugins"],
        url='http://www.lisa-project.net',
        license='MIT',
        author='Julien Syx',
        author_email='julien.syx@gmail.com',
        description='LISA home automation system - Server',
        include_package_data=True,
        namespace_packages=['lisa'],
        scripts = ['lisa/server/lisa-cli'],
        install_requires=listify('requirements.txt'),
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

    from twisted.plugin import IPlugin, getPlugins
    list(getPlugins(IPlugin))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lisa.server.web.weblisa.settings")
    call_command('collectstatic', interactive=False)
