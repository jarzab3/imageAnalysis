// jQuery.noConflict();

var $ = jQuery;


$(document).ready(function () {


    // document.getElementById("myForm").onsubmit = function () {
    // valueURL = document.getElementById("apiUrlID").value;
    // console.log(valueURL);
    // alert(document.getElementById("apiUrl").value);
    // };


// $("#search_form_input").keyup(function(){
//     $("#target1").click(function () {
//
//         apiKey = document.getElementById("apikey").value;
//
//         param = document.getElementById("parameters").value;
//
//         // alert(apiKey);
//         // alert(param);
//
//         var url = "https://www.lugus.co/api/explore/charity/name";
//         var url1 = "https://lugus.co/api/datasearch/company";
//         var url2 = "https://www.lugus.co/api/datasearch/address";
//         var urlS = "https://www.lugus.co/api/explore/charity/name?search_string=gift";
//
//         // alert(valueURL);
//
//
//         $.ajax({
//             url: urlS,
//             type: 'GET',
//             headers: { 'apikey': 'Udi1Yxyb88OtKfH7cZSd'},
//
//             dataType : 'json',
//
//             crossDomain : true,
//             // data: { "string": param, "page": 1},
//
//             contentType: 'application/json; charset=utf-8',
//
//             success: function (response) {
//                 $("#place_for_suggestions").html(response);
//             },
//             error: function (xhr) {
//                 //Do Something to handle error
//             }
//         });
//     });

    function displayJson(obj) {

        var tbl = $("<table/>").attr("id", "mytable");

        $("#result").append(tbl);

        alert(obj.length);

        alert(obj);

        for (var i = 0; i < obj.length; i++) {
            alert(obj[i]);
            // var tr = "<tr>";
            // var td1 = "<td>" + obj[i]["aurn"] + "</td>";
            // var td2 = "<td>" + obj[i]["adress_full"] + "</td>";
            // var td3 = "<td>" + obj[i]["adress_type"] + "</td></tr>";
            //
            // $("#mytable").append(tr + td1 + td2 + td3);
        }
    }

    function IsJsonString(str) {
        try {
            JSON.parse(str);
        } catch (e) {
            return false;
        }
        return true;
    }

    $(function () {
        $('a#sendApi').bind('click', function () {

            $.getJSON($SCRIPT_ROOT + '/_apiQuery', {
                apiQ0: $('p.display-url').text(),
                apiQ1: $('input[name="apikey-in"]').val(),
                apiQ2: $('input[name="string-in"]').val(),
                apiQ3: $('input[name="page-in"]').val()

            }, function (data) {

                obj = JSON.parse(data.result);

                $("#result").text(obj);


            });

            return false;

        });
    });


//    end of the script
});


// function UserAction(url) {
//     alert(url);
//     var xhttp = new XMLHttpRequest();
//     xhttp.open("POST", url, true);
//     xhttp.setRequestHeader("Content-type", "application/json");
//     xhttp.send();
//     var response = JSON.parse(xhttp.responseText);
//     alert(response);
// }
