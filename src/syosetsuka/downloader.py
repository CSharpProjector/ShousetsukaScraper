from typing import TextIO
from urllib.request import urlopen
from bs4 import BeautifulSoup
from novel import Novel
from download_result import DownloadResult

from os import mkdir
from os.path import isdir, isfile, join

from datetime import date

import subprocess


def parse_shousetsu_paragraph_element(p_element: any) -> str:
    if p_element.br is not None:
        return "\n"

    return p_element.text


def parse_shousetsu_page(page: str) -> tuple[str, str]:
    title_: str
    content_: str = ""

    page_soup = BeautifulSoup(page, "html.parser")

    title_element = page_soup.find("p", class_="novel_subtitle")

    if title_element is None:
        raise TypeError("parse_shousetsu_page: Page not valid (not title element found)")

    title_ = title_element.text

    content_element = page_soup.find("div", id="novel_honbun")

    if content_element is None:
        raise TypeError("parse_shousetsu_page: Page not valid (no content element found)")

    for paragraph_element in content_element.find_all("p"):
        content_ += parse_shousetsu_paragraph_element(paragraph_element)

    return title_, content_


def get_page_html(page_url: str) -> any:
    web_url = urlopen(page_url)

    if web_url.getcode() != 200:
        return DownloadResult.BadHtmlStatusCode

    return web_url.read()


def create_novel_folder_metadata(novel: Novel, novel_dir: str):
    joined_dir = join(novel_dir, f"{novel.title} META.txt")

    with open(joined_dir, "w", encoding="utf-8") as fs:
        fs.write(f"{novel.title} metadata -> {date.today()}\n{repr(novel)}")

    subprocess.check_call(["attrib", "+H", joined_dir])


def write_novel_chapter(output_path: str, novel: Novel, page_number: int, title: str, text: str):
    with open(f"{output_path}/{page_number} - {novel.title}.txt", "w", encoding="utf-8") as fs:
        fs.writelines(f"{title}\n{text}")


class ShousetsuDownloader:
    _base_url: str
    _output_folder: str

    def __init__(self, output_folder: str = "novels/", base_url: str = "https://ncode.syosetu.com"):
        self._output_folder = output_folder
        self._base_url = base_url

    def _generate_url_from_ncode(self, ncode: str, page_number: int) -> str:
        return f"{self._base_url}/{ncode}/{page_number}"

    def _create_novel_folder(self, novel: Novel):
        if not isdir(self._output_folder):
            mkdir(self._output_folder)

        novel_path = join(self._output_folder, novel.title)

        if not isdir(novel_path):
            mkdir(novel_path)

        create_novel_folder_metadata(novel, novel_path)

        return novel_path

    def download_page(self, novel: Novel, page_number: int, novel_path: str) -> DownloadResult:
        url_ = self._generate_url_from_ncode(novel.ncode, page_number)
        html_ = get_page_html(url_)

        if html_ is DownloadResult.BadHtmlStatusCode:
            return html_

        title_, contents_ = parse_shousetsu_page(html_)
        write_novel_chapter(novel_path, novel, page_number, title_, contents_)

        return DownloadResult.Success

    def download_novel(self, novel: Novel, out_stream: TextIO = None):
        page_count: int = novel.general_all_no

        novel_path: str = self._create_novel_folder(novel)

        successful_pages: int = 0

        for current_page in range(1, page_count + 1):
            if out_stream is not None:
                out_stream.write(f"Downloading page: {current_page} of {page_count}\t")

            result = self.download_page(novel, current_page, novel_path)

            if result == DownloadResult.Success:
                successful_pages += 1

        if out_stream is not None:
            out_stream.write(f"Successfully downloaded {successful_pages} out of {page_count}\n")
