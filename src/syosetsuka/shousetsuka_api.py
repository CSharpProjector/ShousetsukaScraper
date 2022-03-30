import json
import sys

import requests
import gzip

from sys import getsizeof

from request_creator import create_request
from request_parameter import RequestParameter
from novel import novel_from_response_json
from parsing_result import NovelParsingResult
from typing import Union

API_URL: str = "http://api.syosetu.com/novelapi/api/"
API_ADULT_URL: str = "https://api.syosetu.com/novel18api/api/"


def extract_allcount(allcount_dict: dict) -> Union[int, NovelParsingResult]:
    if "allcount" not in allcount_dict.keys():
        return NovelParsingResult.NoAllCount
    return int(allcount_dict["allcount"])


class ShousetsukaAPI:
    _base_url: str
    _data_usage: int

    url: str

    def __init__(self, url: str = API_URL):
        self.url = url
        self.base_url = self.url + "?out=json&gzip=5&"

        self._data_usage = 0

    def _add_usage(self, response_content):
        self._data_usage += getsizeof(response_content)

    def get_novel(self, ncode: str, limit: int = 1):
        novel_request = create_request(self.base_url, RequestParameter("ncode", str(ncode)),
                                       RequestParameter("lim", str(limit)))

        print(novel_request)

        http_response = requests.get(novel_request)

        self._add_usage(http_response.content)

        http_response.encoding = 'gzip'

        response_content = gzip.decompress(http_response.content).decode("utf-8")

        response_json = json.loads(response_content)

        all_count = extract_allcount(response_json[0])

        if all_count == 0:
            return NovelParsingResult.NoNovelInResponse

        print(response_json)

        with open("dump.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(response_json))

        return novel_from_response_json(response_json)
