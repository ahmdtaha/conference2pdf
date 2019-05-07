import arxiv_search_api
from utils import pdf_utils
import csv
def read_papers(conf_file):
    papers_reader = csv.reader(open(conf_file,'r'))
    papers_headers = next(papers_reader, None)
    accepted_papers = []
    for row in papers_reader:
        accepted_papers.append(row[1])

    return accepted_papers
def main():

    # papers_lst = ['LiveSketch: Query Perturbations for Guided Sketch-based Visual Search',
    #               'Region Proposal by Guided Anchoring']
    conf_file = './conf/cvpr2019.csv'
    papers_lst = read_papers(conf_file);
    filter_keyword = 'metric'
    papers_lst = [paper for paper in papers_lst if ' {} '.format(filter_keyword) in paper.lower()]
    papers_lst = papers_lst[:20] ## download first 20 papers only

    found_lst = []
    for paper in papers_lst:
        saved_as = arxiv_search_api.arxiv_query(paper)
        if saved_as is not None:
            print('{} saved as {}'.format(paper, saved_as))
            found_lst.append(saved_as)

    # pdf_lst = ['./tmp/1.pdf', './tmp/2.pdf']
    print(found_lst)
    pdf_utils.merge_files(found_lst,'cvpr2019.pdf')


if __name__ == '__main__':
    main()