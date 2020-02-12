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
from action_app.controllers.base import Base

@pytest.mark.vcr
def test_it_outputs_to_stdout_by_default(run_app):
    app = run_app('command1', 'node1')
    data, output = app.last_rendered
    assert output.find(data['job'].stdout) != -1

@pytest.mark.vcr
def test_saving_output_to_a_directory(run_app, tmpdir):
    stdout_path = tmpdir.join('node1.stdout')
    app = run_app('command1', 'node1', '-o', str(tmpdir))
    data, output = app.last_rendered
    job = data['job']
    assert output.find(job.stdout) == -1
    assert stdout_path.check()
    assert stdout_path.read().find(job.stdout) != -1

