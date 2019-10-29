# conference2pdf
This python script merges a list of papers (pdf files) into a single pdf. While [pdftk](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/) is a natural alternatives, this script retrieves the conference papers from arxiv before merging them. I mainly implemented it for personal use but I thought may be other people would be interested so I am sharing it on github.

All conferences release a list of accepted papers. Given this list, the script searches arxiv for these papers, download and merge them into a single pdf file.
This reduces the overhead of manual searching for papers and swicthing back and forth between the accepted list and online search results.

# Features
* The script enables filtering papers by keyworks. For example, you can download papers with title containing 'neural'
* [To be added] Enable user to specify the max number of papers to download
* [To be added] Support paper shuffling

### The script limitations 

* The current script searches arxiv only. So, if the paper is not on arxiv or published on arxiv under a different title. It won't be found
* [To be fixed soon] The current script assumes a csv file as input, e.g., ./conf/cvpr2019.csv. This will be fixed soon to support other formats.
* [To be fixed later] Computer vision is my main interest. So I will focus on conferences like CVPR, ICCV, etc. I will try to make the code generic as possible **but If someone interested to support more conferences, you are welcomed.**

## Sample Conferences
* [CVPR 2019 papers - 3GB pdf](https://drive.google.com/file/d/1zomjKnlBqpdXikEhNlggkt72L-ZCcLo7/view?usp=sharing), [Accepted paper list csv file](https://drive.google.com/file/d/1CrBs5Fdz771hP873nBxYDxju5rG1iM49/view?usp=sharing)
* [ICML 2019 papers - 1.3 GB pdf](https://drive.google.com/file/d/1env5gwcG5OcTlGCL_zBmgl6kZpa6Ghsy/view?usp=sharing)
* ICCV 2019 papers [Part 1 - 1GB PDF](https://drive.google.com/file/d/1kkBZvxFmsk6t5iB7CoYUST8gb4DsIzus/view) - [Part 2 - 1GB PDF](https://drive.google.com/file/d/17NTo8Ob6Fs0ky8iXcUAKGq5IoEmFZguj/view) - [Part 3 - 217MB PDF](https://drive.google.com/file/d/1tGwH5MsUYOEHYG6c2W9PQDWe_WXi1REG/view)
* [NeurIPS 2019 papers *Subset*](https://drive.google.com/open?id=12sWcO5gAJqFq3MmPgLOueLbEzOQUYulM). The camera ready papers are not released yet
