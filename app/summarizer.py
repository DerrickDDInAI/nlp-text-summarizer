"""
Python script to summarize small and large text
"""
# =====================================================================
# Import
# =====================================================================

# import internal modules
import re
import requests
import time
from typing import List, Set, Dict, TypedDict, Tuple, Optional

# import 3rd-party modules
import pandas as pd
# from transformers import pipeline
# import gensim
from gensim.summarization import summarize

# import local modules

# load pre-trained summarization pipeline
# global summarizer
# summarizer = pipeline("summarization")

# =====================================================================
# Classes
# =====================================================================

class PipelineSummarizer():
    """
    PipelineSummarizer
    It has 2 attributes: name, xxx
    * name: xxx
    * xxx: xxx
    Class attributes:
    * xxx:
    * xxx:
    """

    # class attributes

    def __init__(
        self,
        xy_position: tuple,
        size=50,
        mass: int = 1,
        name: str = None,
        color: tuple = (0, 0, 255),  # RGB color code for blue
    ) -> None:
        """
        Function to create an instance of PipelineSummarizer class
        By default:
        * xxx if no name is provided
        * xxx
        """
        pass


def pipeline_summarize(text, summarizer, min_length=30, max_length=130):
    """
    Function to summarize a text
    """
    # summarize text
    summary = summarizer(text, min_length=min_length, max_length=max_length, do_sample=False)

    return summary[0]["summary_text"]


# =====================================================================
# Main Function
# =====================================================================

def main():
    book_html_link = "https://www.gutenberg.org/files/103/103-h/103-h.htm"

    # scrape book page
    response = requests.get(book_html_link)
    print(book_html_link, response.status_code)

    # scrape
    soup = bs(response.text, 'html.parser')
    results = soup.find_all(['h4', 'p'])
    text = [result.text for result in results]
    book = ' '.join(text)


    # With gensim

    # start timer
    start_time = time.time()

    # pass text corpus to summarizer
    summary = summarize(book_text)

    # stop timer and compute the execution time
    end_time = time.time()
    diff_time = (end_time - start_time)
    print(f"\nTime to summarize: {diff_time:.2f} seconds")
    
    # export to txt file
    with open("extractive_summary_around_the_world.txt", "w") as file:
        file.write(summary)

# =====================================================================
# Run
# =====================================================================

# execute main() if you directly run this program
if __name__ == '__main__':
    main()