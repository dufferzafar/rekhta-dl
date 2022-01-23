#!/usr/bin/env python3

"""
Rekhta Ebook Downloader.

Usage: rekhta <ebook-url>

"""

import os
import re

from io import BytesIO


import click
import slugify
import requests

from PIL import Image
from tqdm import tqdm
from pyquery import PyQuery as pq


def decrypt_page(sim, data):
    dim = Image.new("RGB", (data["PageWidth"], data["PageHeight"]))

    s = 50  # Size of the square

    for p in data["Sub"]:

        sx = p['X1'] * (s + 16)
        sy = p['Y1'] * (s + 16)
        sbox = (sx, sy, sx + s, sy + s)

        dx = p['X2'] * s
        dy = p['Y2'] * s
        dbox = (dx, dy, dx + s, dy + s)

        dim.paste(im=sim.crop(sbox), box=dbox)

    return dim

def download_ebook(url):
    """Extract page names and page ids from Rekhta Ebook page"""

    if "ebook-detail" in url:
        url = url.replace("ebook-detail", "ebooks")

    html = requests.get(url).content.decode("ascii", "ignore")
    bookname = pq(html)("bdi").text()

    # TODO: Extract & use author name as well
    filename = slugify.slugify(bookname, separator=' ').title() + ".pdf"

    if os.path.exists(filename):
        print(f"File already exists: '{filename}'")
        return

    print(f"Downloading '{filename}' from {url}")

    BOOKID_RE = re.compile(r"var bookId = \"(.*)\";")
    bookid = BOOKID_RE.search(html).group(1)

    PAGE_RE = re.compile(r"var pages = \[(.*?)\];", re.DOTALL)
    pagenames = PAGE_RE.search(html).group(1).split()
    pagenames = [p[1:-1] for p in pagenames if p != ',']

    PAGEIDS_RE = re.compile(r"var pageIds = \[(.*?)\];", re.DOTALL)
    pageids = PAGEIDS_RE.search(html).group(1).split()
    pageids = [p[1:-1] for p in pageids if p != ',']


    # Download Images
    pages = []
    for pagename, pageid in tqdm(zip(pagenames, pageids)):
        pages.append(download_page(bookid, pagename, pageid))

    # Save as PDF
    # TODO: Handle already existing files
    pages[0].save(filename, save_all=True, append_images=pages[1:])

    print()

def download_page(bookid, pagename, pageid):
    page_img_url = f"https://ebooksapi.rekhta.org/images/{bookid}/{pagename}"
    page_img = Image.open(BytesIO(requests.get(page_img_url).content))

    page_data_url = f"https://ebooksapi.rekhta.org/api_getebookpagebyid/?atky=pns&pgi={pageid}"
    page_data = requests.get(page_data_url).json()

    return decrypt_page(page_img, page_data)


@click.command()
@click.argument('url', required=True)
def main(url):
    download_ebook(url)


if __name__ == '__main__':
    main()
