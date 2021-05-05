"""
Default text for the text area form
"""
source: str = """
Source: 
Shrivarsheni. “Text Summarization Approaches for NLP – Practical Guide with Generative Examples.” ML+, 24 October 2020,
https://www.machinelearningplus.com/nlp/text-summarization-approaches-nlp-example/ (visited on 5 May 2021)
"""

default_text: str = """Introduction
When you open news sites, do you just start reading every news article? Probably not. We typically glance the short news summary and then read more details if interested. Short, informative summaries of the news is now everywhere like magazines, news aggregator apps, research sites, etc.

Well, It is possible to create the summaries automatically as the news comes in from various sources around the world.

The method of extracting these summaries from the original huge text without losing vital information is called as Text Summarization. It is essential for the summary to be a fluent, continuous and depict the significant.

In fact, the google news, the inshorts app and various other news aggregator apps take advantage of text summarization algorithms.
In this post, I discuss and use various traditional and advanced methods to implement automatic Text Summarization.

Image showing the Text Summarization

Types of Text Summarization
Text summarization methods can be grouped into two main categories: Extractive and Abstractive methods
Extractive Text Summarization
It is the traditional method developed first. The main objective is to identify the significant sentences of the text and add them to the summary. You need to note that the summary obtained contains exact sentences from the original text.

Abstractive Text Summarization

It is a more advanced method, many advancements keep coming out frequently(I will cover some of the best here). The approach is to identify the important sections, interpret the context and reproduce in a new way. This ensures that the core information is conveyed through shortest text possible. Note that here, the sentences in summary are generated, not just extracted from original text.

In the next sections, I will discuss different extractive and abstractive methods. At the end, you can compare the results and know for yourself the advantages and limitations of each method.
"""