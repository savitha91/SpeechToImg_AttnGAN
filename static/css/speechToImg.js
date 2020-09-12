//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording
var url;
var filename;
var textData;
var blob1;
// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
//var pauseButton = document.getElementById("pauseButton");

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
//pauseButton.addEventListener("click", pauseRecording);
function startRecording() {
	console.log("recordButton clicked");

	/*
		Simple constraints object, for more advanced audio features see
		https://addpipe.com/blog/audio-constraints-getusermedia/
	*/

    var constraints = { audio: true, video:false }

 	/*
    	Disable the record button until we get a success or fail from getUserMedia()
	*/

	recordButton.disabled = true;
	stopButton.disabled = false;
	//pauseButton.disabled = false

	/*
    	We're using the standard promise based getUserMedia()
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

		/*
			create an audio context after getUserMedia is called
			sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
			the sampleRate defaults to the one set in your OS for your playback device
		*/
		audioContext = new AudioContext();

		//update the format
		document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"

		/*  assign to gumStream for later use  */
		gumStream = stream;

		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);

		/*
			Create the Recorder object and configure to record mono sound (1 channel)
			Recording 2 channels  will double the file size
		*/
		rec = new Recorder(input,{numChannels:1})

		//start the recording process
		rec.record()

		console.log("Recording started");

	}).catch(function(err) {
	  	//enable the record button if getUserMedia() fails
    	recordButton.disabled = false;
    	stopButton.disabled = true;
    	//pauseButton.disabled = true
	});
}

function pauseRecording(){
	console.log("pauseButton clicked rec.recording=",rec.recording );
	if (rec.recording){
		//pause
		rec.stop();
		pauseButton.innerHTML="Resume";
	}else{
		//resume
		rec.record()
		pauseButton.innerHTML="Pause";

	}
}

function stopRecording() {
	console.log("stopButton clicked");

	//disable the stop button, enable the record too allow for new recordings
	stopButton.disabled = true;
	recordButton.disabled = false;
	//pauseButton.disabled = true;

	//reset button just in case the recording is stopped while paused
	//pauseButton.innerHTML="Pause";

	//tell the recorder to stop the recording
	rec.stop();

	//stop microphone access
	gumStream.getAudioTracks()[0].stop();

	//create the wav blob and pass it on to createDownloadLink
	rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {
    blob1 = blob
	url = URL.createObjectURL(blob);
	var au = document.createElement('audio');
	var li = document.createElement('li');
	au.id = "audio"
	au.controls = true;
	au.src = url;
	li.appendChild(au);
	recordingsList.appendChild(li);
	proceedFunc()

}
function proceedFunc(){
    var img = document.createElement('button')
    img.id = 'proceed'
	img.innerHTML = "Proceed"
    img.onclick=sendBlob
    genImgButtonID.appendChild(img)
}
function sendBlob(){
    stopButton.disabled = true;
	recordButton.disabled = true;
	//pauseButton.disabled = true;
    const res = fetch("/processSpeech", {
    method: "post", //posting data to the server
    body: blob1
    }).then(function(response){
    if (response.status !== 200) {
        console.log(`Looks like there was a problem. Status code: ${response.status}`);
        return;
    }response.json().then(function (data) {
        var divElement = document.createElement('div')
        var pElement1 = document.createElement('p')
        var strongElement = document.createElement("strong")
        strongElement.innerHTML = "Did you say :  "
        pElement1.appendChild(strongElement)
        var pElement2 = document.createElement('p')
        textData = data
        var strongElement2 = document.createElement("strong")
        strongElement2.innerHTML = textData + " ? "
        //pElement2.innerHTML = textData
        pElement2.appendChild(strongElement2)
        console.log("Did you say ", textData)
        proceedButton = document.getElementById("proceed")
        proceedButton.disabled = true;
        divElement.appendChild(pElement1)
        divElement.appendChild(pElement2)
        speechRec.appendChild(divElement)
        var div_buttons = document.createElement('div')
        div_buttons.id = 'controls'
        var yesButton = document.createElement('button')
        yesButton.id = 'yes'
	    yesButton.innerHTML = "Yes, generate image"
	    yesButton.onclick = generateImg
	    var noButton = document.createElement('button')
        noButton.id = 'no'
	    noButton.innerHTML = "No, record again"
	    noButton.onclick = reRecord
	    div_buttons.appendChild(yesButton)
	    div_buttons.appendChild(noButton)
        speechRec.appendChild(div_buttons)
        });
    })
    .catch(function (error) {
        console.log("Fetch error: " + error);
      });
}

function generateImg(){
         noButton =  document.getElementById("no")
         noButton.disabled = true;
         let speechData = {
            speech: textData
         };
         const res = fetch("/genImg", {
             method: "post",
             body :JSON.stringify(textData)
         }).then(function(response){
        if (response.status !== 200) {
            console.log(`Looks like there was a problem. Status code: ${response.status}`);
            return;
        }response.json().then(function (data) {
            var pElement = document.createElement('p')
            pElement.innerHTML = ""
            imgDiv.appendChild(pElement)
            var figElement = document.createElement('figure')
            var imgElement = document.createElement('img')
            imgElement.src = Flask.url_for("static", {"filename": "output/0_s_0_g2.png"})
            imgElement.height = "470"
            imgElement.width = "500"
            figElement.appendChild(imgElement)
            imgDiv.appendChild(figElement)});
            yesButton = document.getElementById("yes")
            yesButton.disabled = true;
         })
        .catch(function (error) {
             console.log("Fetch error: " + error);
        });
}

function reRecord(){
        location.reload();
}
