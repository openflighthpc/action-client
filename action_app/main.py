
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import ActionAppError
from .controllers.base import Base

from jsonapi_client import Session

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

# Configuration Defaults
CONFIG = init_defaults('flight_action')
# CONFIG['flight_action']['foo'] = 'bar'


class ActionApp(App):
    """Action Client primary application."""

    class Meta:
        label = 'action_app'

        # configuration defaults
        config_defaults = CONFIG

        # look for configs under the user facing key
        config_section = 'flight-action'

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

        # register handlers
        handlers = [
            Base
        ]

    def __init__(self):
        App.__init__(self)
        self.session = None

    def open_session(self):
        self.session = Session('http://127.0.0.1:6304', schema=Schema)

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
        ('pre_setup', open_session),
        ('post_setup', add_commands),
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

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
