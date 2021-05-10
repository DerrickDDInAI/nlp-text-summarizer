"""
Python script to summarize small and large text
"""
# =====================================================================
# Import
# =====================================================================

# import internal modules
import re
import requests
from typing import List, Set, Dict, TypedDict, Tuple, Optional

# import 3rd-party modules
from bs4 import BeautifulSoup as bs
from gensim.summarization import summarize as gensim_summarize
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline


# import local modules
from app.decorators import timer

# load pre-trained summarization pipeline
# global summarizer
# summarizer = pipeline("summarization")

# =====================================================================
# Functions
# =====================================================================

# decorator to measure runtime of function
@timer
def gensim_summary(text, ratio=0.2, word_count=None, split=False):
    """
    Function to perform extractive text summarization
    with Gensim
    * ratio = proportion of summary compared with text
    * word_count = number of words in summary
    """
    return gensim_summarize(text, ratio, word_count, split)


# =====================================================================
# Classes
# =====================================================================

class TransformersPipeline():
    """
    TransformersPipeline class is a wrapper for HuggingFace transformers
    """
    def __init__(self, model_identifier: str, pipeline) -> None:
        """
        Function to create an instance of PipelineSummarizer class
        model_identifier = string identifier of model:
        e.g. "facebook/bart-large-cnn"
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_identifier)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_identifier)
        self.summarizer = pipeline("summarization", model=self.model, tokenizer=self.tokenizer)


    def chunk_text(self, text: str) -> List[str]:
        """
        Function to chunk long text
        according to tokenizer.model_max_length
        """
        # Get max number of inputs possible for model
        max_chunk_len = self.tokenizer.model_max_length

        # Replace [.?!] by [.?!]<EOS> 
        pattern = re.compile(r'(?P<punctuation>[.?!])')
        text = pattern.sub('\g<punctuation><EOS>', text)

        # split in sentences
        sentences: str = text.split('<EOS>')

        # create list and current_chunk counter
        chunks: List[str] = []
        current_chunk: int = 0
        
        for sentence in sentences:
            if len(chunks) == current_chunk + 1:

                # if adding a sentence doesn't exceed max_chunk_len 
                if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk_len:

                    # add tokens to current chunk
                    chunks[current_chunk].extend(sentence.split(' '))
                
                # else add tokens to next chunk
                else:
                    current_chunk += 1
                    chunks.append(sentence.split(' '))
            
            # add tokens to 1st chunk
            else:
                chunks.append(sentence.split(' ')[:max_chunk_len])

        # for each chunk, join tokens to make a single string
        for i in range(len(chunks)):
            chunks[i] = ' '.join(chunks[i])
            
        return chunks

    # decorator to measure runtime of function
    @timer
    def summarize(self, text, min_length=30, max_length=200):
        """
        Function to summarize a text 
        or list of text(to deal with long documents)
        """
        # summarize text
        summaries = self.summarizer(text, min_length=min_length, max_length=max_length, do_sample=False)
        summary = ' '.join([summary['summary_text'] for summary in summaries])
        
        return summary

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

    # Extractive summary
    extractive_summary = gensim_summary(book)

    # Instantiate TransformersPipeline class
    facebook_bart_large_cnn = TransformersPipeline("facebook/bart-large-cnn", pipeline)
    extractive_summary_chunks = facebook_bart_large_cnn.chunk_text(extractive_summary)

    summary = facebook_bart_large_cnn.summarize(extractive_summary_chunks)
    
    # export to txt files
    with open("static/data/extractive_summary_gensim.txt", "w") as file:
        file.write(extractive_summary)
    
    with open("static/data/summary_facebook_bart.txt", "w") as file:
        file.write(summary)

# =====================================================================
# Run
# =====================================================================

# execute main() if you directly run this program
if __name__ == '__main__':
    main()