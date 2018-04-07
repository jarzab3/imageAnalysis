// jQuery.noConflict();

var $ = jQuery;

$(document).ready(function () {

    function requestAPI(arg, url) {

        $.getJSON($SCRIPT_ROOT + url, {
            apiQ0: arg

        }, function (data) {

            console.log(data.result);

        });

        return false;
    }

    // function requestAPI(arg, url) {
    //
    //     $.get(url, function (data) {
    //         $(".result").html(data);
            //
            // alert(data);
        // });
        //
        // return false;
    // }


    var slider = document.getElementById("myRange");
    var output = document.getElementById("sliderInfo");
    output.innerHTML = slider.value;

    var sliderURL = "_apiQueryBar";

    slider.oninput = function () {
        var sliderValue = this.value / 10;
        output.innerHTML = sliderValue;

        requestAPI(sliderValue, sliderURL);

    }

    var grayScaleURL = "_apiQueryColor";
    var substractorURL = "_apiQueryBack";
    var videoRecordURL = "_apiQueryRecord";

    var enableGrayScale = $('#grayscale');
    var enableSubstractor = $('#backSubtractor');
    var enableRecording = $('#recordVideo');

    var enableGrayScaleVal = enableGrayScale.is(':checked');
    var enableSubstractorVal = enableSubstractor.is(':checked');
    var enableRecordingVal = enableRecording.is(':checked');


    var modalButton = $('#modal-button');

    $(function () {

        //TODO fix slide value on open up


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

        });


        modalButton.click(function () {

            setStatus();

        });

    });

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
