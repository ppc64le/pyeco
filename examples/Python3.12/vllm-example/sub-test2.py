# transfoermers with wrapt

import wrapt
from transformers import pipeline

# Define a decorator using wrapt
@wrapt.decorator
def log_call(wrapped, instance, args, kwargs):
    print(f"Calling function: {wrapped.__name__}")
    return wrapped(*args, **kwargs)

@log_call
def main():
    # Load sentiment analysis pipeline
    sentiment_analyzer = pipeline("sentiment-analysis")

    # Input text
    text = "I love working with Python. It's so intuitive!"

    # Analyze sentiment
    result = sentiment_analyzer(text)

    # Print result
    print(f"Text: {text}")
    print(f"Sentiment: {result[0]['label']} (Score: {result[0]['score']:.2f})\n")

    # Input 2
    text2 = "I hate vegetables. They tasts bad!"

    # Analyze sentiment
    result2 = sentiment_analyzer(text2)

    # Print result2
    print(f"Text: {text2}")
    print(f"Sentiment: {result2[0]['label']} (Score: {result2[0]['score']:.2f})")

if __name__ == "__main__":
    main()