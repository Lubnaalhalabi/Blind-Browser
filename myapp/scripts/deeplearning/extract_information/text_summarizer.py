from transformers import pipeline
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

class TextSummarizer:
    def __init__(self, model_name='sshleifer/distilbart-cnn-12-6'):
        """
        Initialize the TextSummarizer with the specified summarization model.

        :param model_name: Name of the summarization model to use (default is 'sshleifer/distilbart-cnn-12-6')
        """
        self.summarizer = pipeline('summarization', model=model_name)

    def summarize_text(self, text, sumarize):
        """
        Summarize the given text using the initialized summarization model.

        :param text: Text to summarize
        :parm sumarization approach
        :return: Summarized text
        """
        if sumarize == 'Ab':
            # Calculate the input length (approximate word count)
            input_length = len(text.split())
            # Adjust max_length based on input length
            max_length = min(150,  max(5,input_length))
            # Summarize the text using the pipeline
            summary = self.summarizer(text, max_length=max_length, min_length=2, do_sample=False)
            return summary[0]['summary_text']
        else: 
            # Load spaCy model
            nlp = spacy.load("en_core_web_sm")

            # Process the text
            doc = nlp(text)

            # Extract sentences and their importance
            sentences = [sent.text for sent in doc.sents]
            scores = {sent: len([token for token in nlp(sent) if token.text.lower() not in STOP_WORDS]) for sent in sentences}

            # Sort sentences by importance
            sorted_sentences = sorted(scores, key=scores.get, reverse=True)

            # Select the top 2 sentences as the summary
            summary = ' '.join(sorted_sentences[:2])
            return summary
