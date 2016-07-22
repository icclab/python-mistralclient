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

from oslo_utils import uuidutils

from mistralclient.api import base


class DelayTolerantWorkload(base.Resource):
    resource_name = 'DelayTolerantWorkload'


class DelayTolerantWorkloadManager(base.ResourceManager):
    resource_class = DelayTolerantWorkload

    def create(self, name, workflow_identifier, deadline, job_duration,
               workflow_input=None, workflow_params=None):
        self._ensure_not_empty(
            name=name,
            workflow_identifier=workflow_identifier
        )

        data = {
            'name': name,
            'deadline': deadline,
            'job_duration': job_duration
        }

        if uuidutils.is_uuid_like(workflow_identifier):
            data.update({'workflow_id': workflow_identifier})
        else:
            data.update({'workflow_name': workflow_identifier})

        if workflow_input:
            data.update({'workflow_input': json.dumps(workflow_input)})

        if workflow_params:
            data.update({'workflow_params': json.dumps(workflow_params)})

        return self._create('/delay_tolerant_workloads', data)

    def list(self):
        return self._list('/delay_tolerant_workloads',
                          response_key='delay_tolerant_workloads')

    def get(self, name):
        self._ensure_not_empty(name=name)

        return self._get('/delay_tolerant_workloads/%s' % name)

    def delete(self, name):
        self._ensure_not_empty(name=name)

        self._delete('/delay_tolerant_workloads/%s' % name)
