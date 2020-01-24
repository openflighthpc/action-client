
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version

VERSION_BANNER = """
Run a command on a node or over a group %s
%s
""" % (get_version(), get_version_banner())

class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'Run a command on a node or over a group'

        # text displayed at the bottom of --help output
        epilog = 'Usage: flight-action <command> [--group] <name>'

        # controller level arguments. ex: 'action_app --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } )
        ]

    def add_command(cmd):
        def runner(self):
            data = {
                'command':  cmd.id,
                'name':     self.app.pargs.name
            }

            self.app.render(data, 'command1.jinja2')
        runner.__name__ = cmd.id
        ex(
            help=cmd.summary,
            description=cmd.description,
            arguments = [
                (['name'], dict(help='The name of the node (or group)'))
            ]
        )(runner)
        setattr(Base, cmd.id, runner)

