import os
import io
from PyPDF2 import PdfFileMerger, PdfFileReader
import subprocess

def merge_files(pdf_lst,write_filepath):
    command = ['pdftk']
    command.extend(pdf_lst)
    command.extend(['output',write_filepath])
    subprocess.call(command) # for py3 use subprocess.run(command)

def merge_files_pypdf2(pdf_lst,write_filepath): ## fails for some pdf files
    merger = PdfFileMerger(strict=False)
    for filename in pdf_lst:
        if not os.path.exists(filename):
            print('Something is wrong with this file')


        with open(filename, 'rb') as pdf_file:
            # bytes_content = io.BytesIO(filename)
            fileReader = PdfFileReader(pdf_file)
            print(fileReader.getNumPages())
            try:
                print(fileReader.documentInfo)
                merger.append(fileReader)
            except:
                print('Something wrong with {}'.format(filename))

    with open(write_filepath, 'wb') as fileobj:
        merger.write(fileobj)
