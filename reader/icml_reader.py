import os
import hashlib
import requests
import numpy as np
import pandas as pd
from utils import os_utils
from search_engines import common
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):


    def __init__(self):
        HTMLParser.__init__(self)
        self.papers_titles = []
        self.valid_tag = False

    def handle_starttag(self, tag, attrs):

        if tag == 'div':
            if len(attrs) == 1 and len(attrs[0]) == 2 and attrs[0][1] == 'maincardBody':
                # print('handle_starttag', tag, attrs)
                self.valid_tag = True


    def handle_endtag(self, tag):
        self.valid_tag = False
        # print(tag)


    def handle_data(self, data):
        if self.valid_tag:
            # print('handle_data',data)
            self.papers_titles.append(data)


def read_papers(link):

    response = requests.get(link)
    data = response.content
    # print(data)

    parser = MyHTMLParser()
    parser.feed(str(data))

    print('found {} paper title'.format(len(parser.papers_titles)))
    os_utils.txt_write('../conf/icml2019.txt',parser.papers_titles)
    # csv_data = {'Title': parser.papers_titles, 'Link': parser.papers_links,'Name':papers_hash}
    # df = pd.DataFrame.from_dict(csv_data)
    # df.to_csv('./papers_cvpr2019.csv')

if __name__ == '__main__':
    read_papers('https://icml.cc/Conferences/2019/Schedule?type=Poster')
