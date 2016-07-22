# -*- coding: utf-8 -*-
#
# Copyright (c) 2016. Zuercher Hochschule fuer Angewandte Wissenschaften
# All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

import mock

from mistralclient.api.v2 import delay_tolerant_workload
from mistralclient.commands.v2 import delay_tolerant_workload as \
    delay_tolerant_cmd
from mistralclient.tests.unit import base


DTW_DICT = {
    'name': 'dtw_test',
    'workflow_name': 'flow1',
    'workflow_input': {},
    'workflow_params': {},
    'deadline': '2016-07-22T00:00:00',
    'job_duration': 4,
    'created_at': '1',
    'updated_at': '1'
}

DTW = delay_tolerant_workload.DelayTolerantWorkload(mock, DTW_DICT)


class TestCLIDTW(base.BaseCommandTest):
    @mock.patch('argparse.open', create=True)
    def test_create(self, mock_open):
        self.client.cron_triggers.create.return_value = DTW
        mock_open.return_value = mock.MagicMock(spec=open)

        result = self.call(
            delay_tolerant_cmd.Create,
            app_args=['dtw_test', 'flow1', '--deadline', '2016-07-22T00:00:00',
                      '--params', '{}', '--job-duration', '4']
        )

        self.assertEqual(
            (
                'dtw_test', 'flow1', {}, '2016-07-22T00:00:00', 4, '1', '1'
            ),
            result[1]
        )

    def test_list(self):
        self.client.delay_tolerant_workloads.list.return_value = [DTW]

        result = self.call(delay_tolerant_cmd.List)

        self.assertEqual(
            [(
                'dtw_test', 'flow1', {}, '2016-07-22T00:00:00', 4, '1', '1'
            )],
            result[1]
        )

    def test_get(self):
        self.client.delay_tolerant_workloads.get.return_value = DTW

        result = self.call(delay_tolerant_cmd.Get, app_args=['name'])

        self.assertEqual(
            (
                'dtw_test', 'flow1', {}, '2016-07-22T00:00:00', 4, '1', '1'
            ),
            result[1]
        )

    def test_delete(self):
        self.call(delay_tolerant_cmd.Delete, app_args=['name'])

        self.client.delay_tolerant_workloads.delete.assert_called_once_with(
                'name'
        )

    def test_delete_with_multi_names(self):
        self.call(delay_tolerant_cmd.Delete, app_args=['name1', 'name2'])

        self.assertEqual(2,
                         self.client.delay_tolerant_workloads.delete.call_count)
        self.assertEqual(
            [mock.call('name1'), mock.call('name2')],
            self.client.delay_tolerant_workloads.delete.call_args_list
        )
