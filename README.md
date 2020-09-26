# Speech To Image app using FLASK API

Speech to Image is an open-source project aimed to "Visualize anything we say", powered by PyTorch, SpeechRecognition,Attention GAN and Flask. We record user voice from the browser using Javascript MediaRecorder API, recognise the audio using SpeechRecognition API and check with user, if what he/she said is recognized correctly. If the audio is recognized right, the identified text is then passed to Attention GAN model (pretrained on Bird's dataset), which generates an image that matches the text. In current stage,user can record something related to birds and visualise the same

## Demo
![AppDemo](/Demo/captured.gif)


## App Structure
Application has the following folders and files :

1. AppFlask.py - Main script for launching our Flask app
2. AttnGan - This folder contains util files, pretained model(.pth files), eval and model code of the AttentionGAN 
2. static - This folder contains css file, javascript file and output folder(where the recognised text and generated images are stored)
3. templates - This folder contain HTML file
4. config.py - This file contains pre-trained model, output location information
5. Dockerfile - Used while deploying app in docker
6. Procfile - When deploying app in Heroku, this file is required 
7. requirements.txt - This file contains all the required libraries

## Run app locally
1. git clone https://github.com/savitha91/SpeechToImg_AttnGAN.git
2. cd SpeechToImg_AttnGaN
3. Create new conda environment for our project and install the libraries from requirements.txt
   1. conda create --name speech2img python
   2. conda activate speech2img
   3. pip install -r requirements.txt 
4. python AppFlask.y
5. Navigate to http:localhost:5000 for the app (Flask runs on port 5000 by default)

#### Common error
OSError: [Errno 48] Address already in use.

Solution -
1. Find the process :    $sudo lsof -i :5000
2. Kill the process id : $sudo kill -9 <pid>

## Deploy app as Docker image and run 
1. git clone https://github.com/savitha91/SpeechToImg_AttnGAN.git
2. cd SpeechToImg_AttnGaN
3. docker build -f Dockerfile -t speechtoimg .
4. docker run -p 5002:5000 -ti speechtoimg
5. Navigate to http://localhost:5002 for the app (We have mapped default port 5000 to port 5002)

## Application UI using streamlit API
Please check the branch "streamlitApp"

## About This Project
This project is a part of Data Science Incubator (Summer 2020) organized by Made With ML. We constantly look for better models. We welcome your contributions and please contact us if you do!

The core idea behind the project is to use the app as a visualisation tool while planning house constructions, where the requirements can be given by the customer(record the voice) and the app shows an image of the same.

#### On-going task 
1. The current state of the project is it works fine for Birds images, working on ObjectGAN model trained on COCO dataset to generate random image with multiple objects
2. Building a Seq2Seq model for Speech recognition on MELD-training dataset

### Documentation
Topics researched, issues faced, identified solutions, topics currently working on, can be found in the attached document - Speech2Image_MML.docx

## Acknowledgements
1. SpeechRecognition API to recognise what user said. 
https://pypi.org/project/SpeechRecognition/
2. Capture audio from browser using Javascript MediaRecorder API
https://medium.com/jeremy-gottfrieds-tech-blog/javascript-tutorial-record-audio-and-encode-it-to-mp3-2eedcd466e78
3. Pre-trained AttnGAN model is used to generate image 
https://github.com/taoxugit/AttnGAN
4. Resolve address alread in use error
https://medium.com/@madhav_46395/find-and-kill-process-locking-port-5000-or-5001-on-mac-bc0257ce614b




