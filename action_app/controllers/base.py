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

from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version

from jsonapi_client import ResourceTuple, Inclusion

from action_app.exceptions import MissingNodesError

import os

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
        def render_job(render, job, directory):
            # Setup the top level rendering scope
            data = { 'job': job,
                     'node': job.node,
                     'long_format': False if directory else True }

            if directory:
                if not os.path.exists(directory): os.mkdir(directory)
                with open(os.path.join(directory, job.node.name + '.stdout'), 'w+') as f:
                    f.write(job.stdout)
                with open(os.path.join(directory, job.node.name + '.stderr'), 'w+') as f:
                    f.write(job.stderr)

            render(data, 'job.mustache')

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

            # Error if no jobs where returned
            if len(ticket.jobs) == 0:
                if self.app.pargs.group:
                    msg = 'Could not execute any jobs as the nodes do not exist'
                else:
                    msg = 'Could not execute the job as the node does not exist'
                raise MissingNodesError(msg)

            for j in ticket.jobs: render_job(self.app.render, j, self.app.pargs.output)

        runner.__name__ = cmd.id
        ex(
            help=cmd.summary,
            description=cmd.description,
            arguments = [
                (['-g', '--group'], { 'action': 'store_true',
                    'help': "Run over the group given by 'name'" }),
                (['-o', '--output'], { 'metavar': 'DIRECTORY',
                    'help': "Save the results within this directory"}),
                (['name'], dict(help='The name of the node (or group)'))
            ]
        )(runner)
        setattr(Base, cmd.id, runner)

