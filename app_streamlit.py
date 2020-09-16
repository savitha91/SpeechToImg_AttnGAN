import speech_recognition as sr
import streamlit as st
from AttnGan.eval import *
def getTextFromAudio(wavFile, model):
    with sr.WavFile(wavFile) as source:
        audio = model.record(source)
        value = model.recognize_google(audio)
        try:
            text = model.recognize_google(audio) # recognize speech using Google Speech Recognition
            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                print(u"You said {}".format(text).encode("utf-8"))
            else:  # this version of Python uses unicode for strings (Python 3+)
                print("You said {}".format(text))
                # just print text : st.write will be appended
                st.write("You said : {}".format(text))
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
    return text

def saveTextToFile(text):
    with open(cfg.TEXTFILE, 'w') as f:
        f.write(text)


def getImageFromText(caption):
    with st.spinner('Generating Image...'):
        # load word dictionaries
        wordtoix, ixtoword = word_index()
        text_encoder, netG = models(len(wordtoix))
        generate(caption, wordtoix, ixtoword, text_encoder, netG)
        #os.system("python ./AttnGAN/code/main.py --cfg ./AttnGAN/code/cfg/eval_bird.yml --gpu -1")
        time.sleep(5)
    st.success('Done!')
    image = Image.open(cfg.OUTPUT_IMG_PATH + '/0_s_0_g2.png')
    st.image(image, use_column_width=True)
    print("TASK COMPLETED SUCCESSFULLY")


def recordAudio(model, wavFile):
    try:
        mic = sr.Microphone(sample_rate=16000)
        with mic as source:
            model.adjust_for_ambient_noise(source)
        print("Say something!")
        st.subheader("Say something")
        with mic as source:
            audio = model.listen(source)
        st.write("Got it!")
        with open(wavFile, 'wb') as f:
            f.write(audio.get_wav_data())
    except KeyboardInterrupt:
        pass


def main():
    page = st.sidebar.selectbox("Choose a page", ['Speech to Image', 'Score', 'Speech to Text Validation'])
    if page == 'Speech to Image':
        st.header("Speech to Image")
        st.subheader('Say what image you need. We will show it')
        if st.button("Record"):
            model = sr.Recognizer()
            recordAudio(model,cfg.WAVFILE)
            text = getTextFromAudio(cfg.WAVFILE,model)
            saveTextToFile(text)
            getImageFromText(text)
    elif page == 'Score':
        st.header("TO BE DONE")
    else:
        st.header("TO BE DONE")



if __name__ == "__main__":
    main()