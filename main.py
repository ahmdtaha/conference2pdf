import arxiv_search_api
from utils import pdf_utils
from reader import csv_reader
from argparse import ArgumentParser


def filter_papers(papers,keyword):
    filter_keyword = keyword
    papers_lst = [paper for paper in papers if ' {} '.format(filter_keyword) in paper.lower()]
    return papers_lst


def main(cfg):

    # papers_lst = ['LiveSketch: Query Perturbations for Guided Sketch-based Visual Search',
    #               'Region Proposal by Guided Anchoring']

    conf_file = cfg.input
    if conf_file[-3:] == 'csv':
        papers_lst = csv_reader.read_papers(conf_file);
    else:
        raise NotImplementedError('{} format is not an supported format'.format(conf_file[-3]))

    papers_lst = filter_papers(papers_lst,'metric')
    if cfg.max > -1:
        papers_lst = papers_lst[:cfg.max] ## download first 20 papers only

    found_lst = []
    for paper in papers_lst:
        saved_as = arxiv_search_api.arxiv_query(paper)
        if saved_as is not None:
            print('{} saved as {}'.format(paper, saved_as))
            found_lst.append(saved_as)
    # print(found_lst)
    pdf_utils.merge_files(found_lst,cfg.output)

if __name__ == '__main__':
    parser = ArgumentParser(description='Conf2pdf script')
    # Required.
    parser.add_argument(
        '--output', required=True, type=str,
        help='Where to generate the output pdf file')

    parser.add_argument(
        '--input', required=True, type=str,
        help='Where is the input list of accepted papers? '
             'This can be csv, txt or open access py file (http://openaccess.thecvf.com/CVPR2018.py)')

    parser.add_argument(
        '--max', required=True, type=int, default=-1,
        help='What is the maximum number of papers to download')


    args = [
        '--output','cvpr2019.pdf',
        '--input','./conf/cvpr2019.csv',
        '--max', '20',
    ]
    cfg = parser.parse_args(args)
    main(cfg)