import urllib
import difflib

def similar(seq1, seq2):
    return difflib.SequenceMatcher(a=seq1.lower(), b=seq2.lower()).ratio() > 0.9

def download_pdf(url,save_as_file):

    response = urllib.request.urlopen(url)
    file = open(save_as_file, 'wb')
    file.write(response.read())
    file.close()
