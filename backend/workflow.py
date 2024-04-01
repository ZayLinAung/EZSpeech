import google.generativeai as genai
import os
from openai import OpenAI
import os
from google.cloud import translate_v2 as translate
from translate import translate_text
from generate import get_response
from generate import sample_sentiment_text


LANGUAGE_ONE = "en"

LANGUAGE_TWO = "zh"

USER_ONE_INPUT = ""

def translate_language_from_text_file(path_to_text_file, outtext):
    f = open(path_to_text_file, "r")

    #print(translate_text(outtext, f.read()))

    return translate_text(outtext, f.read())


def main():

    choice = 0
    sentiminates = None

    #Text file is in Language One 
    #trasnlates language one to english
    english_translatation = translate_text("en", USER_ONE_INPUT)

    #gets responses to the inpout of user one in english
    english_prompts = get_response(english_translatation)

    response_one = english_prompts["translatedText"].split()[0]
    response_two = english_prompts["translatedText"].split()[1]
    response_three = english_prompts["translatedText"].split()[2]

    #translate each response into language 2
    language_two_prompt_1 = translate_text(LANGUAGE_TWO, response_one)
    language_two_prompt_2 = translate_text(LANGUAGE_TWO, response_two)
    language_two_prompt_3 = translate_text(LANGUAGE_TWO, response_three)

    if (choice == 1):
        sentiminates = sample_sentiment_text(response_one)
    
    elif (choice == 2):
        sentiminates = sample_sentiment_text(response_two)

    elif (choice == 3):
        sentiminates = sample_sentiment_text(response_three)

    elif choice == 4: #user wants to input their own output
        pass



    print("ONE\n")
    print(response_one)
    print(response_one[3:-1])

    print("TWO\n")
    print(response_two)
    print(response_two[3:-1])

    print("THREE\n")
    print(response_three)
    print(response_three[3:-1])

    print(translate_text("en", response_one[3:-1]))

    #get response choices
    #english_prompts = get_response(english_translatation)

    #translate prompts to out language


    #pass


if __name__ == "__main__":
    main()