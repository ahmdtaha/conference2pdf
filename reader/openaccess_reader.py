
import requests
import numpy as np
# from HTMLParser import HTMLParser
from html.parser import HTMLParser

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
        if tag == 'dt':
            print('New Paper starts\n--------------------------')
            self.parsing_paper = True
            self.counter = 0
        elif tag == 'form':
            self.skip_enabled = True
            return
        elif self.skip_enabled :
            return
        # elif tag == 'dd':
        print("{}: Encountered a start tag:".format(self.counter+1), tag,attrs)
        self.counter+=1

        if self.parsing_paper and len(attrs) == 1 and attrs[0][0] == 'href' and self.counter == 6:
            link = attrs[0][1]
            self.papers_links.append(link)
            if len(self.papers_links) != len(self.papers_titles):
                print(self.papers_titles[-1],self.papers_titles[-2])
                print('That should not happen')
            # if not self.first_word[-1] in link:
            #     print(self.first_word[-1],self.papers_titles[-1])

    def handle_endtag(self, tag):
        if tag == 'form':
            self.skip_enabled = False
            return
        elif self.skip_enabled :
            return
        print("Encountered an end tag :", tag)


    def handle_data(self, data):
        if self.skip_enabled:
            return
        print("Encountered some data  :", data)
        if self.parsing_paper and len(data) > 3 and self.counter == 3:
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
    print('found {} paper title and {} paper links'.format(len(parser.papers_titles),len(parser.papers_links)))


if __name__ == '__main__':
    read_papers('http://openaccess.thecvf.com/CVPR2019.py')