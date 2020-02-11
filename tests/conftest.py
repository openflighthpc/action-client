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

"""
PyTest Fixtures.
"""

import yaml
import pytest
from cement import fs

from action_app.main import ActionAppTest

@pytest.fixture
def run_app(*argv):
    def _run_app():
        with ActionAppTest(argv=argv) as a:
            a.run()
            return a

    return _run_app

@pytest.fixture(scope='session')
def commands_yaml():
    with open('tests/fixtures/commands.yaml') as file:
        return yaml.load(file, Loader=yaml.FullLoader)

@pytest.fixture(scope='module')
def vcr_config():
    return {
        "filter_headers": [('authorization', 'REDACTED')],
    }

