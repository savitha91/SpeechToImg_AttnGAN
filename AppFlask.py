from flask import Flask, request, jsonify, render_template, make_response
import numpy as np
import json
from eval import *
import speech_recognition as sr
from flask_jsglue import JSGlue
app =Flask(__name__)
jsglue = JSGlue(app)
from datetime import datetime

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    #r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def home():
    return render_template('speechToImg.html')

def getTextFromAudio(wavFile, model):
    with sr.WavFile(wavFile) as source:
        audio = model.record(source)
        value = model.recognize_google(audio)
        try:
            text = model.recognize_google(audio) # recognize speech using Google Speech Recognition
            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                print(u"You said {}".format(text).encode("utf-8"))
            else:  # this version of Python uses unicode for strings (Python 3+)
                print("You said {}".format(text))
                # just print text : st.write will be appended
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
    return text


def saveTextToFile(text):
    with open(cfg.TEXTFILE, 'w') as f:
        f.write(text)

def getImageFromText(caption):
    wordtoix, ixtoword = word_index()
    text_encoder, netG = models(len(wordtoix))
    generate(caption, wordtoix, ixtoword, text_encoder, netG)
    time.sleep(5)
    print("TASK COMPLETED SUCCESSFULLY")

@app.route('/processSpeech', methods=['POST'])
def process_speech():
    f = open(cfg.WAVFILE, 'wb')
    f.write(request.data)
    f.close()
    model = sr.Recognizer()
    text = getTextFromAudio(str(cfg.WAVFILE), model)
    res = make_response(jsonify(text))
    return res


@app.route('/genImg', methods=['POST'])
def generate_img():
    print("Enterred")
    text = request.data.decode()
    saveTextToFile(text)
    getImageFromText(text)
    return make_response(jsonify("SUCCESS"))



if __name__ == "__main__":
    app.run(debug=True)