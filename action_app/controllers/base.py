
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version

from jsonapi_client import Session
from action_app.records import Schema

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
        epilog = 'Usage: action_app command1 --foo bar'

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
        arguments = [
            (['name'], {})
        ]
    )(runner)
    setattr(Base, cmd.id, runner)

kwargs = { 'headers': { 'Accept': 'application/vnd.api+json' } }
with Session('http://127.0.0.1:6304', request_kwargs=kwargs) as s:
    cmds = s.get('commands').resources
    for c in cmds: add_command(c)

