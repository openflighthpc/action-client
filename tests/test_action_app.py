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

import vcr
import pytest
from pytest import raises
from action_app.main import ActionAppTest
from action_app.exceptions import MissingNodesError
from jsonapi_client.exceptions import DocumentError

@pytest.mark.vcr()
def test_forbidden(run_app):
    with raises(DocumentError):
        run_app()

@pytest.mark.vcr('test/cassettes/commands.yaml')
def test_adds_commands(run_app, commands_yaml):
    app = run_app()
    commands = app.controller._get_exposed_commands()
    assert list(commands_yaml.keys()) == commands

@pytest.mark.vcr
def test_missing_node(run_app):
    with raises(MissingNodesError):
        run_app('command1', 'missing')

@pytest.mark.vcr
def test_missing_group(run_app):
    with raises(MissingNodesError):
        run_app('command1', '--group', 'missing1,missing2')

