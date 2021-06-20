from typing import Dict, List
import requests

from ..models import DaemonID
from .containers import ContainerStore
from ..excepts import Runtime400Exception
from ..models.enums import UpdateOperation


class FlowStore(ContainerStore):
    _kind = 'flow'

    def _add(self, port_expose: int, **kwargs) -> Dict:
        """Sends `post` request to `mini-jinad` to create a Flow.

        :param port_expose: port expose for container flow
        :param kwargs: keyword args
        :return: response from mini-jinad"""
        try:
            r = requests.post(
                url=f'{self.host}/{self._kind}',
                params={'port_expose': port_expose},
                json=self.params,
            )
            if r.status_code != requests.codes.created:
                raise Runtime400Exception(
                    f'{self._kind.title()} creation failed \n{"".join(r.json()["body"])}'
                )
            return r.json()
        except requests.exceptions.RequestException as ex:
            self._logger.error(f'{ex!r}')
            raise Runtime400Exception(
                f'{self._kind.title()} creation failed: {r.json()}'
            )

    def update(
        self,
        id: DaemonID,
        kind: UpdateOperation,
        dump_path: str,
        pod_name: str,
        shards: int = None,
    ) -> Dict:
        """Sends `put` request to `mini-jinad` to execute a command on a Flow.

        :param id: flow id
        :param kind: type of update command to execute (dump/rolling_update)
        :param dump_path: the path to which to dump on disk
        :param pod_name: pod to target with the dump request
        :param shards: nr of shards to dump
        :return: response from mini-jinad"""
        try:
            params = {
                'kind': kind,
                'dump_path': dump_path,
                'pod_name': pod_name,
                'shards': shards,
            }
            r = requests.put(url=f'{self.host}/{self._kind}', params=params)

            if r.status_code != requests.codes.ok:
                raise Runtime400Exception(
                    f'{self._kind.title()} update failed \n{"".join(r.json()["body"])}'
                )
            return r.json()

        except requests.exceptions.RequestException as ex:
            self._logger.error(f'{ex!r}')
            raise Runtime400Exception(f'{self._kind.title()} update failed: {r.json()}')

    def _delete(self) -> None:
        """Sends `delete` request to `mini-jinad` to terminate a Flow."""
        try:
            r = requests.delete(url=f'{self.host}/{self._kind}')
            if r.status_code != requests.codes.ok:
                raise Runtime400Exception(
                    f'{self._kind.title()} deletion failed \n{"".join(r.json()["body"])}'
                )
        except requests.exceptions.RequestException as ex:
            raise Runtime400Exception(
                f'{self._kind.title()} deletion failed: {r.json()}'
            )
