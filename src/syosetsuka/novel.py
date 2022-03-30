import dataclasses
import types

from dataclasses import dataclass
from typing import Type
from parsing_result import NovelParsingResult

import json


@dataclass
class Novel:
    title: str
    ncode: str
    userid: int
    writer: str
    story: str
    biggenre: int
    genre: int
    gensaku: str
    keyword: str
    general_firstup: str
    general_lastup: str
    novel_type: int
    end: int
    general_all_no: 286
    length: int
    time: int
    isstop: int
    isr15: int
    isbl: int
    isgl: int
    iszankoku: int
    istensei: int
    istenni: int
    pc_or_k: int
    global_point: int
    daily_point: int
    weekly_point: int
    monthly_point: int
    quarter_point: int
    yearly_point: int
    fav_novel_cnt: int
    impression_cnt: int
    review_cnt: int
    all_point: int
    all_hyoka_cnt: int
    sasie_cnt: int
    kaiwaritu: int
    novelupdated_at: str
    updated_at: str


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def is_all_count_in_json_list(json_list: list[dict]) -> bool:
    for dictionary_item in json_list:
        if "allcount" in dictionary_item.keys():
            return True

    return False


def novel_from_json_dict(json_dict: dict):  # -> Type[Novel, NovelParsingResult]:
    if not isinstance(json_dict, dict):
        raise TypeError("NovelFromJsonDict: json_dict not a dictionary")

    novel_instance = Novel(**json_dict)

    #json.dumps(novel_instance, cls=EnhancedJSONEncoder)

    return novel_instance


def novels_from_json_list(json_list: list):  # -> Type[list[Novel], NovelParsingResult]:
    novel_list = []

    print(json_list)
    for novel in json_list:
        print(novel)
        novel_instance = novel_from_json_dict(novel)

        if isinstance(novel_instance, NovelParsingResult):
            return novel_instance

        novel_list.append(novel_instance)

    return novel_list


def novel_from_response_json(json_object):  # -> Type[Novel, list[Novel], NovelParsingResult]:
    if json_object is None:
        raise TypeError("NovelFromResponseJson: json_object was None")

    if not isinstance(json_object, list):
        return novel_from_json_dict(json_object)

    if len(json_object) < 2:
        if not is_all_count_in_json_list(json_object):
            return NovelParsingResult.NoAllCount
        return NovelParsingResult.NoNovelInResponse

    new_json_list = json_object.copy()
    new_json_list.pop(0)

    return novels_from_json_list(new_json_list)
