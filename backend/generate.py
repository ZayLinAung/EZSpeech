from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
    Image,
    Part,
)

import os
import vertexai
import google.generativeai as genai
import os
from openai import OpenAI
from google.cloud import language_v2
import os
#import openai

client = OpenAI(api_key="")

#api_key = ""


#client.api_key = ""

STRANSLATED_STRING = ""


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/prithviseran/Desktop/EZSpeech/backend/API_KEY.json"

def get_response(input):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": input + " Give me 3 possible responses, each response having a different tone of language. Each response must be in format such that: 1: first option (new line) 2: second option (new line) 3: third option"},
    ]
    )

    return response.choices[0].message.content.strip()


def get_response_gemini(prompt):

    multimodal_model = GenerativeModel("gemini-1.0-pro-vision")

    prompt = 'What can you do?'

    contents = [prompt]

    responses = multimodal_model.generate_content(contents, stream=True)
    repsonses_str = []
    for response in responses:
        repsonses_str.append(response.text)

    print(repsonses_str)

    return repsonses_str



    print("\n-------Response--------")
    for response in responses:
        print(response.text, end="")


def sample_sentiment_text(input_string):
    # Create a client
    client = language_v2.LanguageServiceClient()

    # Initialize request argument(s)
    document = language_v2.Document(
        content = input_string, 
        type = language_v2.Document.Type.PLAIN_TEXT
    )

    #document = language_v2.Document()
    #document.content = STRANSLATED_STRING

    request = language_v2.AnalyzeSentimentRequest(
        document=document,
    )

    # Make the request
    response = client.analyze_sentiment(request=request)

    # Handle the response
    return response



def get_tone_and_magnitude(object):

    score = object.document_sentiment.score

    if -0.5 < score < 0.5:
        return (1, 0) # speed, pitch
    elif score < -0.5:
        return (0.5, -0.5) # speed, pitch
    #elif score > 0.5:
    return (1.25, .30) # speed, pitch