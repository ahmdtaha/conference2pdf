import os
import sys

sys.path.append("./")
import hashlib
import requests
import numpy as np
from utils import pdf_utils
from search_engines import common
from html.parser import HTMLParser

from enum import Enum


class Paper(Enum):
    TITLE = 3
    LINK = 6


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.parsing_paper = False
        self.papers_titles = []
        self.papers_links = []
        self.first_word = []
        self.counter = 0
        self.skip_enabled = False

        self.link_cnt = 0
        self.title_cnt = 0

    def handle_starttag(self, tag, attrs):
        if tag == "dt":
            print("New Paper starts\n--------------------------")
            self.parsing_paper = True
            self.counter = 0
        elif tag == "form":
            self.skip_enabled = True
            return
        elif self.skip_enabled:
            return
        # elif tag == 'dd':
        print("{}: Encountered a start tag:".format(self.counter + 1), tag, attrs)
        self.counter += 1

        if (
            self.parsing_paper
            and len(attrs) == 1
            and attrs[0][0] == "href"
            and self.counter == Paper.LINK.value
        ):
            link = attrs[0][1]
            self.papers_links.append(link)
            if len(self.papers_links) != len(self.papers_titles):
                print(self.papers_titles[-1], self.papers_titles[-2])
                print("That should not happen")
            # if not self.first_word[-1] in link:
            #     print(self.first_word[-1],self.papers_titles[-1])

    def handle_endtag(self, tag):
        if tag == "form":
            self.skip_enabled = False
            return
        elif self.skip_enabled:
            return
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        if self.skip_enabled:
            return
        print("Encountered some data  :", data)
        if self.parsing_paper and len(data) > 3 and self.counter == Paper.TITLE.value:
            pre_len = len(self.papers_titles)
            if len(self.papers_titles) == len(self.papers_links):
                self.papers_titles.append(data)
            else:
                self.papers_titles[-1] += data

            # self.first_word.append(data.split()[0])
            # post_len = len(self.papers_titles)
            # if post_len != pre_len + 1:
            #     print(data)


def read_papers(openaccess_url):
    response = requests.get(openaccess_url)
    data = response.content
    # print(data)

    parser = MyHTMLParser()
    parser.feed(str(data))

    np.argmin([len(paper) for paper in parser.papers_titles])
    print(parser.papers_titles)
    print(
        "found {} paper title and {} paper links".format(
            len(parser.papers_titles), len(parser.papers_links)
        )
    )
    if len(parser.papers_titles) != len(parser.papers_links):
        print("Something is wrong")
        quit()

    import pandas as pd

    saved_papers = []
    papers_hash = []
    for paper_title, paper_link in zip(parser.papers_titles, parser.papers_links):
        title_hash = hashlib.sha1(paper_title.encode("utf-8")).hexdigest()
        papers_hash.append(title_hash)
        tmp_save_dir = "./tmp"
        if not os.path.exists(tmp_save_dir):
            os.makedirs(tmp_save_dir)
        save_filepath = "{}/{}.pdf".format(tmp_save_dir, title_hash)
        saved_papers.append(save_filepath)
        if os.path.exists(save_filepath):
            continue

        common.download_pdf(
            "http://openaccess.thecvf.com/{}".format(paper_link), save_filepath
        )

    csv_data = {
        "Title": parser.papers_titles,
        "Link": parser.papers_links,
        "Name": papers_hash,
    }
    df = pd.DataFrame.from_dict(csv_data)
    df.to_csv("./papers_iccv2021.csv")

    output_pdf = "./iccv_2021.pdf"
    pdf_utils.merge_files(saved_papers, output_pdf)


if __name__ == "__main__":
    read_papers("https://openaccess.thecvf.com/ICCV2021?day=all")
