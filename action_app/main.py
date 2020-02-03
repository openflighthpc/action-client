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

from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import ActionAppError
from .controllers.base import Base

from os.path import dirname, join

from jsonapi_client import Session
from jsonapi_client.exceptions import DocumentError

from requests.auth import AuthBase
from requests.exceptions import ConnectionError

Schema = {
    'commands': { 'properties': {
        'summary': { 'type': 'string' },
        'description': { 'type': 'string' },
        'name': { 'type': 'string' }
    }},
    'nodes': { 'properties': {
        'name': { 'type': 'string' }
    }},
    'groups': { 'properties': {
        'name': { 'type': 'string' }
    }},
    'tickets': { 'properties': {
        'true': {},
        'jobs': { 'relation': 'to-many', 'resource': ['jobs'] },
        'context': { 'relation': 'to-one', 'resource': ['nodes', 'groups'] },
        'command': { 'relation': 'to-one', 'resource': ['commands'] }
    }},
    'jobs': { 'properties': {
        'stdout': { 'type': 'string' },
        'stderr': { 'type': 'string' },
        'status': { 'type': 'integer' },
        'node': { 'relation': 'to-one', 'resource': ['nodes'] }
    }}
}

class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, req):
        req.headers['Authorization'] = 'Bearer ' + self.token
        return req

# Configuration Defaults
CONFIG = init_defaults('flight_action', 'log.logging')
CONFIG['flight_action']['base_url'] = 'http://localhost:6304'
CONFIG['flight_action']['jwt_token'] = ''
CONFIG['log.logging']['level'] = 'info'

class ActionApp(App):
    """Action Client primary application."""

    class Meta:
        # Defines the config paths of the label (among other things)
        label = 'flight-action'

        # look for configs under the user facing key
        config_section = 'flight_action'

        # configuration defaults
        config_defaults = CONFIG


        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'mustache'
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yaml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'mustache'

        # sets the template directory
        template_dirs = [join(dirname(__file__), 'templates')]

        # register handlers
        handlers = [
            Base
        ]

    def __init__(self):
        App.__init__(self)
        self.session = None

    def open_session(self):
        self.session = Session(
                self.config.get('flight_action', 'base_url'),
                schema=Schema,
                request_kwargs={ 'auth': BearerAuth(self.config.get('flight_action', 'jwt_token')) })

    def close_session(self):
        self.session.close()

    def add_commands(self):
        cmds = self.session.get('commands').resources
        for c in cmds: Base.add_command(c)

    # the following hooks are used to interact with the server
    # they do the following:
    # 1. Establish a session with the server
    # 2. Download the commands and adds it to the CLI
    #    NOTE: This is done each time the command is ran
    # *. argparser than runs the action [and assumable uses the session]
    # 3. the session is closed
    Meta.hooks = [
        ('post_setup', open_session),
        ('pre_run', add_commands),
        ('pre_close', close_session)
    ]


class ActionAppTest(TestApp,ActionApp):
    """A sub-class of ActionApp that is better suited for testing."""

    class Meta:
        label = 'action_app'


def main():
    with ActionApp() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except ActionAppError as e:
            print('ActionAppError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except DocumentError as e:
            print(e.response.json()['errors'][0]['detail'])
            app.exit_code = 1

        except ConnectionError:
            print('Could not connect to the upstream service')
            app.exit_code = 1

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
