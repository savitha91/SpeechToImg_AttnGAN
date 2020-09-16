# SpeechToImg_AttnGAN

Speech to Image is an open-source project aimed to "Visualize anything we say", powered by PyTorch, SpeechRecognition,Attention GAN and Flask. We record user voice from the browser using Javascript MediaRecorder API, recognise the audio using SpeechRecognition API and check with user, if what he/she said is recognized correctly. If the audio is recognized right, the identified text is then passed to Attention GAN model (pretrained on Bird's dataset), which generates an image that matches the text. In current stage,user can record something related to birds and visualise the same


## Demo



## App Structure
Application has the following folders and files :

1. AppFlask.py - Main script for launching our Flask app
2. static - This folder contains css, javascript file and output folder, where the recognised text and generated images are stored
3. templates - This folder contain HTML file
4. pretraiend - This folder contains pretrained model files, pickle file required for AttnGAN model
5. miscc - This folder container utility files required for AttnGAN model
6. config.py - This file contains pre-trained model, output location information

## Install and Run in Docker
Clone the repo and navigate to the repo:

git clone https://github.com/savitha91/SpeechToImg_AttnGAN.git
cd SpeechToImg_AttnGAN/
docker build -f Dockerfile -t speechtoimg .
docker run -p 5002:5000 -ti speechtoimg

Navigate to http://localhost:5002 for the app. (Flask runs on port 5000 by default)
The Flask app is run in CPU.

## Run Unit Test
TODO

## About This Project
This project is a part of Data Science Incubator (Summer 2020) organized by Made With ML, jointly developed by Savitha Ramesh and Amit Bhatkal. We constantly look for better generation quality . We welcome your contributions and please contact us if you do!

## Acknowledgements
1. SpeechRecognition API to recognise what user said. 
https://pypi.org/project/SpeechRecognition/
2. Capture audio from browser using Javascript MediaRecorder API
https://medium.com/jeremy-gottfrieds-tech-blog/javascript-tutorial-record-audio-and-encode-it-to-mp3-2eedcd466e78
3. Pre-trained AttnGAN model is used to generate image 
https://github.com/taoxugit/AttnGAN


