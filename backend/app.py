
import queue
import re
import sys
from flask import Flask, render_template, request, flash, redirect, url_for, session
from google.cloud import speech
from transcribe import *
from translate import *
from text_to_speech import *
from generate import *
from workflow import *

import pyaudio

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['GET', 'POST']) 
def translate():

    if request.method == 'POST':
        return redirect('/transcribe/en')

    return render_template('translate.html', content=read_file())

@app.route('/translate2/<test>', methods=['GET']) 
def translate2(test):

    print(request.method)

    my_variable = request.args.get('choice1', '')

    print(type(my_variable))

    return render_template('translate.html', choice1 = test)

@app.route('/transcribe/<language>', methods=['GET', 'POST'])
def transcribe_audio(language):
   
    language_code = language  
    
    client = speech.SpeechClient.from_service_account_file('/Users/prithviseran/Desktop/EZSpeech/easyspeech-418815-aa07c590833f.json')  # Update with your service account path
    
    # Configure speaker diarization
    diarization_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=2,
        max_speaker_count=2
    )
    
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code='en-US',  # Specify multiple languages here
        diarization_config=diarization_config,
        alternative_language_codes=['zh-CN', 'fr-FR']  # Specify alternative languages here
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:  
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)
        
        listen_print_loop(responses, '/Users/prithviseran/Desktop/EZSpeech/backend/static/data/dummy_data.txt')

    return redirect("/translate/fr")


@app.route('/translate/<language>', methods=['GET', 'POST'])
def translate_file(language):
    # get the input and target files
    target = open('/Users/prithviseran/Desktop/EZSpeech/backend/text.txt', 'a')
    input = open('/Users/prithviseran/Desktop/EZSpeech/backend/static/data/dummy_data.txt', 'r')
    # get the entire text file as a list then iterate and translate each string in the list
    lines=[]
    for line in input:
        lines.append(line.strip())
    translated = ''
    for line in lines:
        translated = translate_text(language, line)
        #write the text into this file
        
        target.write(translated['translatedText'] + '\n')
    
    return redirect("/outputprompts/" + language)


def read_file():
    with open('/Users/prithviseran/Desktop/EZSpeech/backend/static/data/dummy_data.txt', 'r') as file:
        return file.read()

def read_translated():
    with open('/Users/prithviseran/Desktop/EZSpeech/backend/text.txt', 'r') as file:
        return file.read()  
#def read_file()


@app.route('/outputprompts/<language>', methods=['GET', 'POST'])
def output_choices(language):

    english_translatation = translate_language_from_text_file("/Users/prithviseran/Desktop/EZSpeech/backend/static/data/dummy_data.txt", "en")
    #print(english_translatation['translatedText'])
    english_prompts = get_response(english_translatation['translatedText'])

    #print(english_prompts)

    response_one = english_prompts.split('\n')[0]
    response_two = english_prompts.split('\n')[1]
    response_three = english_prompts.split('\n')[2]

    language_two_prompt_1 = translate_text(language, response_one)
    language_two_prompt_2 = translate_text(language, response_two)
    language_two_prompt_3 = translate_text(language, response_three)

    print("language_two_prompt_1: ", language_two_prompt_1)
    print("language_two_prompt_2: ", language_two_prompt_2)
    print("language_two_prompt_3: ", language_two_prompt_3)

    prompts = [language_two_prompt_1["translatedText"],
               language_two_prompt_2["translatedText"],
               language_two_prompt_3["translatedText"]]



    f = open("/Users/prithviseran/Desktop/EZSpeech/backend/outprompts.txt", "w")
    f.write(language_two_prompt_1["translatedText"] + '\n' + language_two_prompt_2["translatedText"] + '\n' + language_two_prompt_3["translatedText"] + '\n')
    f.close()

    #redirect(url_for('another_route', my_variable=my_variable))
    return render_template('translate_with_choices.html', choice1 = prompts[0], choice2 = prompts[1], choice3 = prompts[2], content = read_file(), translated_content = read_translated())
#render_template("translate.html", choice1 = prompts[0])

#redirect(url_for('translate', choice1 = "Why?", choice2 = prompts[1], choice3 = prompts[2]))


@app.route('/choice', methods=['GET', 'POST'])
def choice_selected():

    if request.method == "POST":
        f = open("/Users/prithviseran/Desktop/EZSpeech/backend/outprompts.txt", "r")
        lines = f.readlines()
        f.close()

        if "choice1" in request.form:
            translated_text = translate_text('en', lines[0])

            sentiminates = sample_sentiment_text(translated_text)
            speed, pitch = get_tone_and_magnitude(sentiminates)

            print(translated_text["translatedText"])

            text_to_wav('en', translated_text["translatedText"], pitch, speed)
        
        elif "choice2" in request.form:
            translated_text = translate_text('en', lines[1])

            sentiminates = sample_sentiment_text(translated_text)
            speed, pitch = get_tone_and_magnitude(sentiminates)

            text_to_wav('en', translated_text["translatedText"], pitch, speed)

        elif "choice3" in request.form:
            translated_text = translate_text('en', lines[2])
            
            sentiminates = sample_sentiment_text(lines[2])
            speed, pitch = get_tone_and_magnitude(sentiminates)

            text_to_wav('en', translated_text["translatedText"], pitch, speed)
        
        else:
            transcribe_audio_for_speech('fr')

            f = open("/Users/prithviseran/Desktop/EZSpeech/backend/outprompts.txt", "r")
            lines = f.readlines()
            f.close()

            print(lines)

            translated_text = translate_text('en', lines[-1])
            print(translated_text["translatedText"])
            sentiminates = sample_sentiment_text(translated_text["translatedText"])

            speed, pitch = get_tone_and_magnitude(sentiminates)

            text_to_wav('en', translated_text["translatedText"], pitch, speed)
        
        
        print(sentiminates)

        return render_template("translate_with_audio.html", content = read_file(), translated_content = read_translated())
            #lan_code: str, text: str, pitch: float, speed: float
    
    else:

        return redirect("/translate")
        


    
    


"""

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


"""






if __name__ == '__main__':
    app.run()