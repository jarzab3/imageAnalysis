jQuery.noConflict();

var $ = jQuery;

$(document).ready(function () {

    //Generic api call function. This function is used for many calls within this file
    function requestAPI(arg, url) {

        $.getJSON($SCRIPT_ROOT + url, {
            apiQ0: arg

        }, function (data) {

            //Uncomment for debugging
            // console.log(data.result);

        });

        return false;
    }


    //Api call function used for getting list of the files on the server.
    function requestAPIFiles(arg, url) {
        filesList = "";

        $.getJSON($SCRIPT_ROOT + url, {
            apiQ0: arg

        }, function (data) {

            //Uncomment for debugging
            // console.log(data.result);

            list = data.result;
            list.sort();
            list.reverse();

            var filesListElement = $("#files-list");

            filesListElement.empty();
            //Display elements in on the server directory
            var i;
            for (i = 0; i < list.length; i++) {
                var item = list[i];
                filesListElement.append('<li class="list-group-item" style="background: rgba(204, 241, 255, 0.7); font-size: 18px; float: left"">' +
                    '<a href="playVideo/' + item + '" target="_blank">' + item +'</a><a style="float: right; margin-left: 100px;" href="/uploads/' + item + '" target="_blank" role="button" class="btn btn-default">'
                    + '<span class="glyphicon glyphicon-align-left" aria-hidden="true">Play video</span>'
                    + '</a></li>');
            }

            return filesList;

        });

        return false;
    }

    //Slider variables and functions
    var slider = document.getElementById("myRange");
    var output = document.getElementById("sliderInfo");
    output.innerHTML = slider.value;

    var sliderURL = "_apiQueryBar";

    slider.oninput = function () {
        var sliderValue = this.value / 10;
        output.innerHTML = sliderValue;

        requestAPI(sliderValue, sliderURL);

    }

    //Define list of all urls required to retrive data from a server
    var grayScaleURL = "_apiQueryColor";
    var substractorURL = "_apiQueryBack";
    var videoRecordURL = "_apiQueryRecord";
    var getFileListURL = "_apiQueryFileList";

    var enableGrayScale = $('#grayscale');
    var enableSubstractor = $('#backSubtractor');
    var enableRecording = $('#recordVideo');
    var enableRecordingLabel = $('#recording-label');

    var enableGrayScaleVal = enableGrayScale.is(':checked');
    var enableSubstractorVal = enableSubstractor.is(':checked');
    var enableRecordingVal = enableRecording.is(':checked');

    //Define buttons variables
    var modalButton = $('#modal-button');
    var filesButton = $('#files-button');

    $(function () {

        enableGrayScale.change(function () {

            enableGrayScaleVal = enableGrayScale.is(':checked');

            requestAPI(enableGrayScaleVal, grayScaleURL);

        });

        enableSubstractor.change(function () {
            enableSubstractorVal = enableSubstractor.is(':checked');

            requestAPI(enableSubstractorVal, substractorURL);

        });

        enableRecording.change(function () {
            enableRecordingVal = enableRecording.is(':checked');

            requestAPI(enableRecordingVal, videoRecordURL);

            //Animate label text notifying user about recording
            if (enableRecordingVal === true){
                enableRecordingLabel.css("animation", "floatText 1s infinite alternate ease-in-out");
                enableRecordingLabel.text("Video recording in progress");
            }else {
                enableRecordingLabel.css("animation", "");
                enableRecordingLabel.text("Enable video recording");
            }


        });

        //On click for a settings modal button, call setStatus function and set up variables
        modalButton.click(function () {

            setStatus();

        });

        //On click for files button, call api to get list of file in directory on the server where all the files are being stored
        filesButton.click(function () {

            requestAPIFiles(true, getFileListURL)

        });

    });

    //Whenever the settings modal is being open then set up a button and other information accoringly to their real time status
    function setStatus() {

        if (enableGrayScaleVal === true) {
            enableGrayScale.attr('checked', true);
        } else {
            enableGrayScale.attr('checked', false);
        }


        if (enableSubstractorVal === true) {
            enableSubstractor.attr('checked', true);
        } else {
            enableSubstractor.attr('checked', false);
        }

        if (enableRecordingVal === true) {
            enableRecording.attr('checked', true);
        } else {
            enableRecording.attr('checked', false);
        }

    }


//    end of the script
});
