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
