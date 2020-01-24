
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version

from jsonapi_client import ResourceTuple, Inclusion

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
            # Selects the type: nodes or groups
            type = 'groups' if self.app.pargs.group else 'nodes'

            # Build the Ticket Resource
            ticket = self.app.session.create('tickets')
            ticket.command = cmd.id
            ticket.context = ResourceTuple(self.app.pargs.name, type)

            # Manually make the requests and parse the included data
            url = ticket.post_url
            payload = { 'data': ticket.json }
            data = self.app.session.http_request('POST', url, payload)[1]

            # Reassign the ticket from the response
            ticket = self.app.session.read(data).resource

            # Render the jobs to the screen
            for j in ticket.jobs: self.app.render(j, 'job.mustache')

        runner.__name__ = cmd.id
        ex(
            help=cmd.summary,
            description=cmd.description,
            arguments = [
                (['-g', '--group'], { 'action': 'store_true',
                    'help': "Run over the group given by 'name'" }),
                (['name'], dict(help='The name of the node (or group)'))
            ]
        )(runner)
        setattr(Base, cmd.id, runner)

