import json
import googleapiclient.discovery
from googleapiclient.errors import HttpError


class DMClient(object):
    """Deployment Manager client."""

    def __init__(self, project_id: str, zone: str):
        self._project_id = project_id
        self._zone = zone
        self._client = googleapiclient.discovery.build('deploymentmanager', 'v2', cache_discovery=False)

    def get(self, deployment_name):
        try:
            res = self._client.deployments().get(project=self._project_id, deployment=deployment_name).execute()
        except HttpError as e:
            data = json.loads(e.content.decode('utf-8'))
            if data['error']['code'] != 404:
                raise e
            res = None

        return res

    def deploy(self, deployment_name, template, dry_run=False):
        res = self._client.deployments().insert(project=self._project_id, body={
            'name': deployment_name,
            'target': {
                'config': {
                    'content': template,
                }
            },
        }, preview=dry_run).execute()

        return res

    def delete(self, deployment_name):
        res = self._client.deployments().delete(project=self._project_id, deployment=deployment_name).execute()
        return res

    def get_resource(self, deployment_name, resource_name) -> dict:
        try:
            res = self._client.resources().get(project=self._project_id,
                                               deployment=deployment_name,
                                               resource=resource_name).execute()
        except HttpError as e:
            data = json.loads(e.content.decode('utf-8'))
            if data['error']['code'] != 404:
                raise e
            res = None

        return res