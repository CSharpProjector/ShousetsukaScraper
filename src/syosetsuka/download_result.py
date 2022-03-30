from enum import Enum


class DownloadResult(Enum):
    BadHtmlStatusCode = 101
    Success = 200
