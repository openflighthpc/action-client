
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import ActionAppError
from .controllers.base import Base

# Configuration Defaults
CONFIG = init_defaults('flight_action')
# CONFIG['flight_action']['foo'] = 'bar'


class ActionApp(App):
    """Action Client primary application."""

    class Meta:
        label = 'flight-action'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yaml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base
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
