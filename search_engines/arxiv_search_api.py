import os
import urllib
import hashlib
import requests
import xmltodict
from search_engines import common


def arxiv_query(paper_title):
    title_hash = hashlib.sha1(paper_title.encode('utf-8')).hexdigest()
    save_filepath = './tmp/{}.pdf'.format(title_hash)
    if os.path.exists(save_filepath):
        return save_filepath

    urllib.quote_plus = urllib.parse.quote  # A fix for urlencoder to give %20

    # ?search_query=all:{}&start=0&max_results=5
    payload = {'search_query': '{}'.format(paper_title), 'start': '0', 'max_results': '2'}

    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    param = urllib.parse.urlencode(payload)  # encodes the data
    url = 'http://export.arxiv.org/api/query'.format(paper_title)
    # print(param)
    response = requests.get(url, params=param, headers=headers)
    data = response.content
    data = xmltodict.parse(data)
    if data['feed']['opensearch:totalResults']['#text'] == '0':
        print('No results available')
        return None

    num_results = len(data['feed']['entry'])
    # links = [None] * num_results
    for i in range(num_results):
        title = data['feed']['entry'][i]['title']
        if common.similar(title, paper_title):
            possible_links = data['feed']['entry'][i]['link']
            for link in possible_links:
                if link['@type'] == 'application/pdf':
                    pdf_link = link['@href']

                    common.download_pdf(pdf_link, save_filepath)
                    return save_filepath
            # print('{} has link {}'.format(title, pdf_link))

    return None
def main():
    paper_title = 'LiveSketch: Query Perturbations for Guided Sketch-based Visual Search'
    paper_title = 'Region Proposal by Guided Anchoring'
    # paper_title = 'electron'
    # paper_title = urllib.parse.quote(paper_title)
    # print(paper_title)
    # quit()
    saved_as = arxiv_query(paper_title)
    if saved_as is not None:
        print('{} saved as {}'.format(paper_title,saved_as))

if __name__ == '__main__':
    main()