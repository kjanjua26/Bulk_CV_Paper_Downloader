"""
Bulk download CVPR papers.
"""

import argparse
from glob import glob
from tqdm import tqdm
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import glob 
import pandas as pd 
import re

# command line arguments
args_parser = argparse.ArgumentParser()
args_parser.add_argument('--year', help='The year to download papers of', action='store', type=str, required=True)
args_parser.add_argument('--path', help='The save path - to save papers in', action='store', type=str, required=True)
args_parser.add_argument('--conf', help='The conference to download papers of', action='store', type=str)
args = args_parser.parse_args()

year = args.year
download_path = args.path
conf = args.conf

class CVPRDownloader:
    def __init__(self):
        self.url = 'http://openaccess.thecvf.com/CVPR{}.py'.format(year)
        print(self.url)
    
    def get_pdf(self):
        """
        CVPR2018 onwards segregates the paper listings in days first.
        """

        pdf_link = []
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "html.parser")
        titles_ = soup.find_all('dt', attrs={'class':'ptitle'})
        pdfs_ = soup.find_all('dd')
        for i in pdfs_:
            date = i.text.split(' ')[-1].replace(']', '')
            if '[<a href' in str(i):
                link_ = str(i).split('\n')[1].split('=')[1].split(">")[0].replace('"','')
                comp_link = 'http://openaccess.thecvf.com/'+link_+'='+date
                pdf_link.append(comp_link)
        return pdf_link

    def download_file(self, download_url=None):
        """
        Download the papers in the specified folder.
        """

        paper_count = 0
        paper_links = []
        
        if download_url is None:
            r = requests.get(self.url)
        else:
            r = requests.get(download_url)
        
        soup = BeautifulSoup(r.content, "html.parser")
        pdfs_ = soup.find_all('dd')
        for ix in str(pdfs_).split('\n'):
            if '[<a href="content_CVPR_' or '[<a href="content_cvpr_' in ix:
                if 'papers' in ix:
                    paper_count += 1
                    link = ix.split('[<a href="')[-1].split('">')[0]
                    paper_link = 'https://openaccess.thecvf.com/' + link
                    print('Paper: ', paper_link)
                    title = link.split('/')[-1].split('.')[0].split('_CVPR_')[0]
                    try:
                        response = urlopen(paper_link)
                        file = open(download_path + "/{}.pdf".format(title), 'wb')
                    except:
                        print("Paper # {} - {} Failed".format(paper_count, title))

                    file.write(response.read())
                    file.close()
                    print("Paper # {} - {} Done".format(paper_count, title))

    def bulk_download(self):
        year_int = int(year)
        if year_int >= 2018:
            pdf_link = self.get_pdf()
            for xi in range(len(pdf_link)):
                self.download_file(pdf_link[xi])
        else:
            self.download_file()

downloader = CVPRDownloader()
downloader.bulk_download()