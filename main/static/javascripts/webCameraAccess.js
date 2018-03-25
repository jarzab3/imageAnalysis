window.onload = function () {

    // Normalize the various vendor prefixed versions of getUserMedia.
    navigator.getUserMedia = (navigator.getUserMedia ||
        navigator.webkitGetUserMedia ||
        navigator.mozGetUserMedia ||
        navigator.msGetUserMedia);

    // Check that the browser supports getUserMedia.
// If it doesn't show an alert, otherwise continue.
    if (navigator.getUserMedia) {
        // Request the camera.
        navigator.getUserMedia(
            // Constraints
            {
                video: true
            },

            // Success Callback
            function (localMediaStream) {

            },

            // Error Callback
            function (err) {
                // Log the error to the console.
                console.log('The following error occurred when trying to use getUserMedia: ' + err);
            }
        );

    } else {
        alert('Sorry, your browser does not support getUserMedia');
    }


}