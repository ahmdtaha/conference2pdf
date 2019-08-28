import nltk
import numpy as np
from reader import csv_reader
from nltk.corpus import stopwords
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

    all_words = ' '.join(papers_lst).lower().split()
    unique_words = list(set(all_words))
    unique_words_count = np.zeros(len(unique_words))
    stop_words = set(stopwords.words('english'))
    for word in all_words:
        if not word in stop_words:
            word_idx = unique_words.index(word)
            unique_words_count[word_idx] +=1
    sorted_idxs = np.argsort(unique_words_count)[::-1][:100]
    print(unique_words_count[sorted_idxs ])
    print([unique_words[i] for i in sorted_idxs])
    # words, counts = np.unique(np.array(all_words),return_counts=True)
    # print(words[:20])
    # print(counts[:20])

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