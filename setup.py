import sys

from distutils.core import setup
from pip.req import parse_requirements

from distutils.command.install_data import install_data
import shutil

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


class my_install(install_data):
    def run(self):
        install_cmd = self.get_finalized_command('install')
        if install_cmd.root:
            self.install_dir = install_cmd.root
        else:
            self.install_dir = "/"
        install_data.run(self)
        for script in self.get_outputs():
            # Rename name.init in name
            if script.endswith(".init"):
                shutil.move(script, script[:-5])

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("install/requirements.txt")

if __name__ == '__main__':

    setup(
        cmdclass={"install_data": my_install},
        name='lisa-server',
        version='0.1.0.10',
        packages = ['lisa', 'lisa.server', 'twisted.plugins'],
        package_data={
            'twisted': ['plugins/lisa-server_plugin.py'],
        },
        url='http://www.lisa-project.net',
        license='MIT',
        author='Julien Syx',
        author_email='julien.syx@gmail.com',
        description='LISA home automation system',
        include_package_data=True,
        namespace_packages = ['lisa'],
        #install_requires=[str(ir.req) for ir in install_reqs],
        data_files=[('etc/lisa/server', ['lisa/server/configuration/lisa.json.sample']),
                    ('var/log/lisa', ''),
                    #('etc/init.d', ['lisa-server.init']),
                    ],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
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
