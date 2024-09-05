# Blind-Browser
This project aims to help blind people browse web pages using their hearing by segmenting web pages, converting texts to audio, and describing images. It also helps ordinary people quickly browse dense content with the least possible effort by summarizing texts in segmented web pages.
## Description
Blind or visually impaired users can rely on audio to get the content of pages, and regular users can rely on the summary to display the main titles in each piece to save time and effort due to:
  - Using several algorithms to segment web pages with their different designs (traditional methods, methods based on deep learning techniques and image processing).
  - Extracting texts from each piece separately and summarizing them.
  - Describing image pieces using deep learning models.
  - Converting texts, summarizing them and descriptions into audio for blind users.
## Archeticture 
A set of proposed algorithms for segmenting web pages(Clustering, SAM(Segment Anything Model), Mathematical Morphology, Edge Detection) , evaluating those algorithms using DSRandom, then choosing the best model from the LLM (Large-Language Models) using ROUGE (Recall-Oriented Understudy for Gisting Evaluation) to summarize text that extracted from segments,then using a VLM (Vision-Language Models )  to describe the image segments, then wrapping the previous algorithms in a web application based on the principle of structure MTV (Model-Template-View).
## Tools
- Canny
- Moments
- DBSCAN
- KMeans
- SAM
- Mathematical Morphology
- Spacy
- sshleifer/distilbart-CNN-12-6
- salesforce/blip-image-captioning-base
- gTTS (Google Text-to-Speech)
- Python 
- Selenium
- Beautiful Soup
- TfidfVectorizer
- Pandas
- Numpy (Numeric Python)
- Requests
- Transformers
- Gaussian Blur
- Silhouette Analysis
- Hugging Face
- Django
- JavaScript
- jQuery
- HTML
- CSS
