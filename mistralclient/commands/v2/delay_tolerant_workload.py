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

import json
import logging

from osc_lib.command import command

from mistralclient.commands.v2 import base
from mistralclient import utils

LOG = logging.getLogger(__name__)


def format_list(dtw=None):
    return format(dtw, lister=True)


def format(dtw=None, lister=False):
    columns = (
        'Name',
        'Workflow',
        'Params',
        'Deadline',
        'Job Duration',
        'Created at',
        'Updated at'
    )

    if dtw:
        data = (
            dtw.name,
            dtw.workflow_name,
            dtw.workflow_params,
            dtw.deadline,
            dtw.job_duration,
            dtw.created_at,
        )

        if hasattr(dtw, 'updated_at'):
            data += (dtw.updated_at,)
        else:
            data += (None,)
    else:
        data = (tuple('<none>' for _ in range(len(columns))),)

    return columns, data


class List(base.MistralLister):
    """List all DTWs."""

    def _get_format_function(self):
        return format_list

    def _get_resources(self, parsed_args):
        mistral_client = self.app.client_manager.workflow_engine
        return mistral_client.delay_tolerant_workloads.list()


class Get(command.ShowOne):
    """Show specific delay tolerant workload."""

    def get_parser(self, prog_name):
        parser = super(Get, self).get_parser(prog_name)

        parser.add_argument('delay_tolerant_workload',
                            help='delay Tolerant Workload name')

        return parser

    def take_action(self, parsed_args):
        mistral_client = self.app.client_manager.workflow_engine

        return format(mistral_client.delay_tolerant_workloads.get(
            parsed_args.delay_tolerant_workload
        ))


class Create(command.ShowOne):
    """Create new delay tolerant workload."""

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)

        parser.add_argument('name', help='Delay Tolerant Workload name')
        parser.add_argument('workflow_identifier', help='Workflow name or ID')

        parser.add_argument(
            'workflow_input',
            nargs='?',
            help='Workflow input'
        )

        parser.add_argument(
            '--params',
            help='Workflow params',
        )

        parser.add_argument(
            '--deadline',
            type=str,
            help='Delay tolerant workload deadline',
            metavar='YYYY-MM-DDTHH:MM:SS'
        )
        parser.add_argument(
            '--job-duration',
            type=int,
            help="Time to complete delay tolerant workload execution",
        )

        return parser

    @staticmethod
    def _get_file_content_or_dict(string):
        if string:
            try:
                return json.loads(string)
            except Exception:
                return json.load(open(string))
        else:
            return {}

    def take_action(self, parsed_args):
        mistral_client = self.app.client_manager.workflow_engine

        wf_input = self._get_file_content_or_dict(parsed_args.workflow_input)
        wf_params = self._get_file_content_or_dict(parsed_args.params)

        dtw = mistral_client.delay_tolerant_workloads.create(
            parsed_args.name,
            parsed_args.workflow_identifier,
            wf_input,
            wf_params,
            parsed_args.deadline,
            parsed_args.job_duration
        )

        return format(dtw)


class Delete(command.Command):
    """Delete delay tolerant workload."""

    def get_parser(self, prog_name):
        parser = super(Delete, self).get_parser(prog_name)

        parser.add_argument(
            'delay_tolerant_workload',
            nargs='+', help='Name of delay_tolerant_workload(s).'
        )

        return parser

    def take_action(self, parsed_args):
        mistral_client = self.app.client_manager.workflow_engine

        utils.do_action_on_many(
            lambda s: mistral_client.delay_tolerant_workloads.delete(s),
            parsed_args.delay_tolerant_workload,
            "Request to delete delay_tolerant_workloads %s has been accepted.",
            "Unable to delete the specified delay_tolerant_workloads(s)."
        )
