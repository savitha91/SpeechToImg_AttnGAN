# Speech To Image app using Streamlit API
Here, we make use of streamlit api to build the front end. Advantage of using streamlit is UI can be built with just few lines of code. 
We use SpeechRecognition API to record and recognise audio. Attention GAN is used to generate image from the recognised text.

### Demo
![AppDemo](/Demo/streamlitDemo.gif)

### App Structure
Application has the following folders and files :

app_streamlit.py - Main script for launching our streamlit app
AttnGan - This folder contains pre-trained Attention GAN model, pickle files, utility , model and evaluation code
config.py - This file contains pre-trained model, output location information
requirements.txt - This file contains all the required libraries
output - This folder contains file having recognised text and generated images 

### Prerequisites (Mandatory)
Copy the contents of AttnGan folder from master to this branch

### Run app locally
1. git clone https://github.com/savitha91/SpeechToImg_AttnGAN.git
2. git checkout streamlitApp
3. cd SpeechToImg_AttnGaN
4. streamlit run app_streamlit.py
5. Navigate to http://localhost:8501 for the app(streamlit runs on 8501 port by default)

### Deploy app in Docker (and Heroku)
Here,we use SpeechRecognition API to record the audio(unlike the flask app in master , which records audio in browser using MediaRecorder API). 
To deploy the app in server, we need to install dependent libraries like pyaudio, portaudio etc. 

If the host OS is linux, we can consider the base image as https://hub.docker.com/r/binkybong/speech-recognition/. Linux uses ALSA , which provides API for sound card device drivers. This docker image is run using the command "docker run -it -v /dev/snd:/dev/snd centos7-speech /bin/bash". Here, we are mapping the host system /dev/snd folder(which has native sound devices) to the docker image.

In other OS, like MAC, which uses Core Audio sound system, does not have the /dev/snd folder. Hence, it is difficult to send audio from MAC to Centos docker image.

#### TODO
One possible solution is to create AWS EC2 Ubuntu instance, install ALSA drivers , dummy sound card and record audio

### Acknowledgements
1. SpeechRecognition API to recognise what user said. https://pypi.org/project/SpeechRecognition/
2. Pre-trained AttnGAN model is used to generate image https://github.com/taoxugit/AttnGAN
