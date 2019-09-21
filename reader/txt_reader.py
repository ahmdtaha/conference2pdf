from utils import os_utils

def read_papers(conf_file):
    lines = os_utils.txt_read(conf_file)
    accepted_papers = []
    for paper_line in range(0,len(lines ),3):
        print(lines[paper_line])
        accepted_papers.append(lines[paper_line])

    return accepted_papers