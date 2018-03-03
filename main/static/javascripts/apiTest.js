// jQuery.noConflict();

var $ = jQuery;

$(document).ready(function () {

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
