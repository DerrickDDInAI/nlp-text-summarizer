"""
Python script to scrape books from `Project Gutenberg` eBook library
website: https://www.gutenberg.org/
"""

# =====================================================================
# Import
# =====================================================================

# import internal modules
import re
import requests
import time
import random

# import 3rd-party modules
from bs4 import BeautifulSoup as bs
import pandas as pd

# import local modules


# =====================================================================
# Functions
# =====================================================================

def download_page(url):
    """
    Function to 
    - download page 
    - and parse it with BeautifulSoup
    """
    # download page
    response = requests.get(url)
    print(url, response.status_code)
    
    # parse page
    soup = bs(response.content, features="lxml")

    return soup


def get_book_links(soup) -> pd.DataFrame:
    """
    Function to get links of the first 25 books 
    from search page
    """
    # create empty dataframe
    cols = ["title", "author", "link", "book_id"]
    books_df = pd.DataFrame(columns=cols)

    # define base url for links
    base_url = "https://www.gutenberg.org"

    # scrape info
    for rank, element in enumerate(soup.find_all("li", attrs={"class": "booklink"}), start=1):
        title = element.find("span", attrs={"class": "title"}).text
        author = element.find("span", attrs={"class": "subtitle"}).text
        link = base_url + element.find("a", attrs={"class": "link"}).get("href")
        # cover_img_link = base_url + element.find("img", attrs={"class": "cover-thumb"}).get("src")
        book_id = re.findall(r"\d+", link)[0]
        # utf_8_txt_link = f"{base_url}/files/{book_id}/{book_id}-0.txt"
        books_df.loc[rank] = [title, author, link, book_id]
        
    return books_df

def get_book_text(link):
    """
    Function to get book text in plain text UTF-8
    """
    # download book page
    soup = download_page(link)

    # define base url for links
    base_url = "https://www.gutenberg.org"

    # scrape book text link
    book_text_link = base_url + soup.find("a", attrs={"class": "link"}, href=re.compile(r".txt")).get("href")

    # slow down requests frequency to avoid IP ban
    time.sleep(random.uniform(2.0, 3.0))

    # download book text page
    response = requests.get(book_text_link)
    print(book_text_link, response.status_code)
    
    # return book text
    return response.text

def search_books(search) -> pd.DataFrame:
    """
    Function to search for books
    """

    # prepare search query url in required format
    search_book_url = "https://www.gutenberg.org/ebooks/search/?query="
    search_book_url += "+".join(search.split(" "))

    # download page
    soup = download_page(search_book_url)

    return get_book_links(soup)


def get_most_popular_books() -> pd.DataFrame:
    """
    Function to get links of the 25 most popular books 
    (most downloaded from `Project Gutenberg`)
    """
    # download page of most popular books
    url='https://www.gutenberg.org/ebooks/search/?sort_order=downloads'
    soup = download_page(url)

    return get_book_links(soup)


# ============================================================
# Run
# ============================================================

def main():
    """
    Main function
    """
    # input search query
    # search = input("search for books, authors, genre, ...")


    popular_books = get_most_popular_books()
    print(popular_books)
    book_link = popular_books.loc[1, "link"]
    print(book_link)
    book_text = get_book_text(book_link)
    # book_text = get_book_text("https://www.gutenberg.org/ebooks/31547")

    # find index position where metadata from website ends
    metadata_end_idx = book_text.rfind("***",0,1000)
    print(book_text[metadata_end_idx: 1000])


# ============================================================
# Run
# ============================================================

# execute main() if you directly run this program
if __name__ == '__main__':
    main()