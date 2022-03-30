from enum import Enum


class NovelParsingResult(Enum):
    AllCountNone = 101
    InvalidJsonObject = 102
    NoAllCount = 201
    NoNovelInResponse = 202
    NovelDoesntExist = 203
