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

import pytest
from pytest import raises
from action_app.main import ActionAppTest
from jsonapi_client.exceptions import DocumentError

@pytest.mark.vcr()
def test_forbidden(run_app):
    with raises(DocumentError):
        run_app()

# def test_action_app():
#     # test action_app without any subcommands or arguments
#     with ActionAppTest() as app:
#         app.run()
#         assert app.exit_code == 0


# def test_action_app_debug():
#     # test that debug mode is functional
#     argv = ['--debug']
#     with ActionAppTest(argv=argv) as app:
#         app.run()
#         assert app.debug is True


# def test_command1():
#     # test command1 without arguments
#     argv = ['command1']
#     with ActionAppTest(argv=argv) as app:
#         app.run()
#         data,output = app.last_rendered
#         assert data['foo'] == 'bar'
#         assert output.find('Foo => bar')


#     # test command1 with arguments
#     argv = ['command1', '--foo', 'not-bar']
#     with ActionAppTest(argv=argv) as app:
#         app.run()
#         data,output = app.last_rendered
#         assert data['foo'] == 'not-bar'
#         assert output.find('Foo => not-bar')
