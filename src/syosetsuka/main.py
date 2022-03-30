from shousetsuka_api import ShousetsukaAPI
from shousetsuka_api import API_URL
from downloader import ShousetsuDownloader
from novel import Novel

from sys import stdout

def main():
    api_wrapper = ShousetsukaAPI(API_URL)
    novel_downloader = ShousetsuDownloader()

    # novel_data = api_wrapper.get_novel("sdffoij", 10)
    novel_data: list[Novel] = api_wrapper.get_novel("N9669BK")

    novel_ = novel_data[0]

    print(novel_.title)

    novel_downloader.download_novel(novel_, stdout)


if __name__ == "__main__":
    main()
