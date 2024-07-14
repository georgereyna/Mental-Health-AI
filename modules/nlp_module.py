from typing import Dict, Any, List
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

class NLPModule:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.symptom_keywords = {
            'depression': ['sad', 'hopeless', 'depressed', 'unmotivated', 'tired'],
            'anxiety': ['worried', 'anxious', 'nervous', 'panic', 'fear'],
            'insomnia': ['sleepless', 'awake', 'restless', 'tired'],
            'stress': ['overwhelmed', 'stressed', 'pressure', 'tense']
        }

    def preprocess_text(self, text: str) -> List[str]:
        # Convert to lowercase and remove punctuation
        text = re.sub(r'[^\w\s]', '', text.lower())
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stop words and lemmatize
        processed_tokens = [
            self.lemmatizer.lemmatize(token) for token in tokens 
            if token not in self.stop_words
        ]
        
        return processed_tokens

    def extract_symptoms(self, text: str) -> Dict[str, int]:
        processed_text = self.preprocess_text(text)
        symptoms = {}
        
        for symptom, keywords in self.symptom_keywords.items():
            count = sum(1 for word in processed_text if word in keywords)
            if count > 0:
                symptoms[symptom] = count
        
        return symptoms

    def analyze_sentiment(self, text: str) -> str:
        processed_text = self.preprocess_text(text)
        
        positive_words = set(['happy', 'good', 'great', 'better', 'improve'])
        negative_words = set(['sad', 'bad', 'worse', 'difficult', 'hard'])
        
        positive_count = sum(1 for word in processed_text if word in positive_words)
        negative_count = sum(1 for word in processed_text if word in negative_words)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'

    def process_text(self, data: Dict[str, Any]) -> Dict[str, Any]:
        text = data['text']
        processed_tokens = self.preprocess_text(text)
        symptoms = self.extract_symptoms(text)
        sentiment = self.analyze_sentiment(text)
        return {
            'processed_tokens': processed_tokens,
            'symptoms': symptoms,
            'sentiment': sentiment
        }