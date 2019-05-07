import csv

def read_papers(conf_file):
    papers_reader = csv.reader(open(conf_file,'r'))
    papers_headers = next(papers_reader, None)
    accepted_papers = []
    for row in papers_reader:
        accepted_papers.append(row[1])

    return accepted_papers