var $ = jQuery;

$(document).ready(function () {


    var correctVal = 0;
    var incorrectVal = 0;


    var firstVal = Math.floor(Math.random() * 50);
    var secondVal = Math.floor(Math.random() * 50);


    var one = document.getElementById("first");
    var second = document.getElementById("second");


    one.textContent = firstVal;
    second.textContent = secondVal;

    var correct = document.getElementById("correctR");
    var incorrect = document.getElementById("incorrectR");

    correct.textContent = correctVal;
    incorrect.textContent = incorrectVal;

    function gen() {
        firstVal = Math.floor(Math.random() * 50);
        secondVal = Math.floor(Math.random() * 50);
        one.textContent = firstVal;
        second.textContent = secondVal;


    }

    function checkresults(over) {
        // var one = document.getElementById("first");
        // var second = document.getElementById("second");


        var resultVal = document.getElementById("result").value;

        var res = parseInt(resultVal);

        var init = firstVal + secondVal;


        if (res == init) {
            correctVal = correctVal + 1;
            correct.textContent = correctVal;


        } else {
            incorrectVal = incorrectVal + 1;
            incorrect.textContent = incorrectVal;

        }

        document.getElementById("result").value = "";

        gen();

        mainRun(over);

    }

    var run = false;


    function mainRun(over) {

        var timeleft = 10;

        // if (over){
        //     timeleft = 10;
        //
        // }

        if (run) {

            var downloadTimer = setInterval(function () {

                // if (over){
                //     timeleft = 0;
                //     checkresults();
                // }

                document.getElementById("progressBar").value = 10 - --timeleft;
                if (timeleft <= 0) {
                    clearInterval(downloadTimer);
                }

                if (timeleft === 0) {

                    timeleft = 0;

                    checkresults(true);

                }
            }, 2000);

        }
    }


    $("#run").click(function () {
        if (run == false) {
            run = true;

            mainRun(false);

        } else {
            alert("You have already started!")
        }
    });

    $("#check").click(function () {
        if (run == true) {
            checkresults(true);
        } else {
            alert("Please press start button!")
        }

    });


});