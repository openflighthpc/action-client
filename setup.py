
from setuptools import setup, find_packages
from action_app.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='action_app',
    version=VERSION,
    description='Run a command on a node or over a group',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Alces Flight Ltd.',
    author_email='dev@alces-flight.com',
    url='https://github.com/openflighthpc/action-client',
    license='EPL-2.0',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'action_app': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        action_app = action_app.main:main
    """,
)
