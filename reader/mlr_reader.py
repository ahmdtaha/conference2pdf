import os
import hashlib
import requests
import numpy as np
from utils import pdf_utils
from utils import timing_utils
from search_engines import common
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.parsing_paper = False
        self.papers_titles = []
        self.papers_links = []

    def handle_starttag(self, tag, attrs):
        print('start ',tag, attrs)
        if tag == 'p':
            if len(attrs) == 1 and len(attrs[0]) == 2:
                if attrs[0][1] == 'title':
                    self.parsing_paper = True
        if tag == 'a':
            if len(attrs) > 1:
                if attrs[0][0] == 'href' and '.pdf' in attrs[0][1]:
                    if 'supp' in attrs[-1][1].lower():
                        pass ## This is the supplementary material
                    else:
                        self.papers_links.append(attrs[0][1])
                    if len(self.papers_links) != len(self.papers_titles):
                        print('Something went wrong at {} {}'.format(self.papers_titles[-1],self.papers_links[-1]))
                        quit()

    def handle_endtag(self, tag):
        print('end ',tag)
        self.parsing_paper = False
        # if self.parsing_paper:
        #     self.papers_titles.append(data)

    def handle_data(self, data):
        print('data ',data)
        if self.parsing_paper:
            if len(self.papers_titles) == len(self.papers_links):
                self.papers_titles.append(data)
            elif len(self.papers_titles) == len(self.papers_links)+1:
                self.papers_titles[-1] += data
            else:
                print('Something went wrong at {} {}'.format(self.papers_titles[-1], self.papers_links[-1]))
                quit()



def read_papers(openaccess_url):
    response = requests.get(openaccess_url)
    data = response.content
    # print(data)

    parser = MyHTMLParser()
    parser.feed(str(data))

    # np.argmin([len(paper) for paper in parser.papers_titles])
    # print(parser.papers_titles)
    print('found {} paper title and {} paper links'.format(len(parser.papers_titles),len(parser.papers_links)))


    if len(parser.papers_titles) != len(parser.papers_links):
        print('Something is wrong')
        quit()

    import pandas as pd

    saved_papers = []
    papers_hash = []
    with timing_utils.LoopBar(len(parser.papers_titles)) as progress_bar:
        for paper_title, paper_link in zip(parser.papers_titles,parser.papers_links):
            progress_bar.step()
            title_hash = hashlib.sha1(paper_title.encode('utf-8')).hexdigest()
            papers_hash.append(title_hash)
            save_filepath = '../tmp/{}.pdf'.format(title_hash)
            saved_papers.append(save_filepath)
            if os.path.exists(save_filepath):
                continue

            common.download_pdf('{}'.format(paper_link), save_filepath)


    csv_data = {'Title': parser.papers_titles, 'Link': parser.papers_links,'Name':papers_hash}
    df = pd.DataFrame.from_dict(csv_data)
    df.to_csv('./papers_icml2019.csv')

    output_pdf = './icml_2019.pdf'
    pdf_utils.merge_files(saved_papers, output_pdf)

if __name__ == '__main__':
    read_papers('http://proceedings.mlr.press/v97/')