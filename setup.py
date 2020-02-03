#==============================================================================
# Copyright (C) 2020-present Alces Flight Ltd.
#
# This file is part of Action Client.
#
# This program and the accompanying materials are made available under
# the terms of the Eclipse Public License 2.0 which is available at
# <https://www.eclipse.org/legal/epl-2.0>, or alternative license
# terms made available by Alces Flight Ltd - please direct inquiries
# about licensing to licensing@alces-flight.com.
#
# Action is distributed in the hope that it will be useful, but
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, EITHER EXPRESS OR
# IMPLIED INCLUDING, WITHOUT LIMITATION, ANY WARRANTIES OR CONDITIONS
# OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY OR FITNESS FOR A
# PARTICULAR PURPOSE. See the Eclipse Public License 2.0 for more
# details.
#
# You should have received a copy of the Eclipse Public License 2.0
# along with Action Client. If not, see:
#
#  https://opensource.org/licenses/EPL-2.0
#
# For more information on Action Client, please visit:
# https://github.com/openflighthpc/action-client
#===============================================================================


from setuptools import setup, find_packages
from action_app.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='flight-action',
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
