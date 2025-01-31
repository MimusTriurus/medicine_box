import requests
from typing import Union

CRPT_ENDPOINT = 'https://mobile.api.crpt.ru/mobile/check'


class Crpt:
    def __init__(self):
        pass

    def _get(self, content: str, type: str) -> Union[list, dict]:
        return requests.get(f'{CRPT_ENDPOINT}?code={content}&codeType={type}').json()

    def info_from_datamatrix(self, matrix_data: str) -> Union[list, dict]:
        return self._get(matrix_data, 'datamatrix')
