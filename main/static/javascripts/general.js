// jQuery.noConflict();

var $ = jQuery;

$(document).ready(function () {

    function requestAPIAlpha(arg) {

        $.getJSON($SCRIPT_ROOT + '/_apiQueryBar', {
            apiQ0: arg

            }, function (data) {

                console.log(data.result);

            });

            return false;
    }

    var slider = document.getElementById("myRange");
    var output = document.getElementById("sliderInfo");
    output.innerHTML = slider.value;

    slider.oninput = function() {
        var sliderValue = this.value / 10;
      output.innerHTML = sliderValue;

      requestAPIAlpha(sliderValue);

    }


    function requestAPI(arg) {

        $.getJSON($SCRIPT_ROOT + '/_apiQuery', {
                // apiQ0: $('a#sendApi').text()
            apiQ0: arg

            }, function (data) {

                console.log(data.result);

            });

            return false;
    }


    $(function () {

        // $('a#sendApi').bind('click', requestAPI("color"));
        // $('a#sendApi1').bind('click', requestAPI("gray"));


        $('a#sendApi').click(function() {
            requestAPI("gray");
        });

        $('a#sendApi1').click(function() {
            requestAPI("color");
        });

            // $.getJSON($SCRIPT_ROOT + '/_apiQuery', {
            //     apiQ0: $('a#sendApi').text()
            //
            // }, function (data) {
            //
            //     // alert(data.result);
            //     console.log(data.result);
            //
            // });
            //
            // return false;

        // });
    });


//    end of the script
});



$(document).ready(function(){
    $('#characterLeft').text('140 characters left');
    $('#message').keydown(function () {
        var max = 140;
        var len = $(this).val().length;
        if (len >= max) {
            $('#characterLeft').text('You have reached the limit');
            $('#characterLeft').addClass('red');
            $('#btnSubmit').addClass('disabled');
        }
        else {
            var ch = max - len;
            $('#characterLeft').text(ch + ' characters left');
            $('#btnSubmit').removeClass('disabled');
            $('#characterLeft').removeClass('red');
        }
    });
});
