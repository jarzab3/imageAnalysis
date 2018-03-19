const canvas = document.getElementById('gc');
const context = canvas.getContext('2d');
const exportCanvas = document.getElementById("exportCanvas");
const exportContext = exportCanvas.getContext("2d");

// Strings
const version = "v1.0 or something";
var globalColor = "#FFFFFF";

// Numbers
const NUM_PIXELS = parseInt(document.getElementById("canvasSize").innerHTML);
const OFFSET = canvas.width / NUM_PIXELS;
var audioTimer = 0;
var TIME_MAX = 10;

// Booleans
var dragging = false;
var erasing = false;
var timingAudio = false;

// Arrays
var keyMap = [];
var colors = [];
var colorsORIG = [];

for (var i = 0; i < NUM_PIXELS; ++i) {
    colors    [i] = [];
    colorsORIG[i] = [];
    for (var j = 0; j < NUM_PIXELS; ++j) {
        if (i % 2 === j % 2) {
            colors    [i][j] = "#FFF";
            colorsORIG[i][j] = "#FFF";
        }
        else {
            colors    [i][j] = "#FFF";
            // colors    [i][j] = "#777";
            colorsORIG[i][j] = "#FFF";
            // colorsORIG[i][j] = "#777";
        }
    }
}

// Objects
var mouse = {x: 0, y: 0};
var tools =
    {
        brush: true,
        eraser: false,
        identifier: false
    };

// Audio

window.onload = function () {
    const fps = 30;
    setInterval(function () {
        Update();
        Draw();
    }, 1000 / fps);
    onkeydown = onkeyup = function (e) {
        keyMap[e.keyCode] = e.type == "keydown";
    }
    canvas.addEventListener('mousedown', CheckClick);
    canvas.addEventListener('mouseup', CheckClick2);
    canvas.addEventListener('mousemove', function (e) {
        mouse.x = CheckMousePos(e).x;
        mouse.y = CheckMousePos(e).y;
    });
    Init();
};

function CheckMousePos(e) {
    const rect = canvas.getBoundingClientRect();
    const root = document.documentElement;
    const mouseX = e.clientX - rect.left - root.scrollLeft;
    const mouseY = e.clientY - rect.top - root.scrollTop;
    return {x: mouseX, y: mouseY};
}

function CheckClick() {
    // When you click, this happens.
    dragging = true;
}

function CheckClick2() {
    dragging = false;
}

function Init() {
    context.webkitImageSmoothingEnabled = false;
    context.mozImageSmoothingEnabled = false;
    context.imageSmoothingEnabled = false;
    exportContext.webkitImageSmoothingEnabled = false;
    exportContext.mozImageSmoothingEnabled = false;
    exportContext.imageSmoothingEnabled = false;
    // document.getElementById( "colorPicker" ).value = "#00FFFF";
    document.getElementById("colorPicker").value = "#000000";
    console.log("Version " + version + " has been loaded successfully!");
}

function Update() {
    // Update things here
    if (keyMap[69]) {
        // SetErasing( true );
        SetTool("eraser");
    }
    if (keyMap[66]) {
        // SetErasing( false );
        SetTool("brush");
    }
    if (keyMap[73]) {
        // IdentifyColor();
        SetTool("identifier");
    }
}

function Draw() {
    // Draw things here
    globalColor = document.getElementById("colorPicker").value;
    // Rect( 0,0,canvas.width,canvas.height,"#000" );
    var drawX = Math.floor(mouse.x);
    var drawY = Math.floor(mouse.y);
    while (drawX % OFFSET != 0) {
        --drawX;
    }
    while (drawY % OFFSET != 0) {
        --drawY;
    }
    if (dragging) {
        // Rect( drawX,drawY,100,100,"#0FF" );
        if (tools.brush) {
            colors[drawY / OFFSET][drawX / OFFSET] = globalColor;
            exportContext.fillStyle = globalColor;
            exportContext.fillRect(drawX / OFFSET, drawY / OFFSET, 1, 1);
        }
        else if (tools.eraser) {
            colors[drawY / OFFSET][drawX / OFFSET] = colorsORIG[drawY / OFFSET][drawX / OFFSET];
        }
        else if (tools.identifier) {
            IdentifyColor();
        }
    }
    for (var i = 0; i < colors.length; ++i) {
        for (var j = 0; j < colors[i].length; ++j) {
            Rect(j * OFFSET, i * OFFSET, OFFSET, OFFSET, colors[i][j]);
        }
    }

    var outlineColor = "#0FF";

    if (tools.brush) {
        outlineColor = "#0FF";
    }
    else if (tools.eraser) {
        outlineColor = "#F00";
    }
    else if (tools.identifier) {
        outlineColor = "#0F0";
    }

    const offset = 3;
    Rect(drawX - offset, drawY, offset, OFFSET, outlineColor);
    Rect(drawX, drawY - offset, OFFSET, offset, outlineColor);
    Rect(drawX + OFFSET, drawY, offset, OFFSET, outlineColor);
    Rect(drawX, drawY + OFFSET, OFFSET, offset, outlineColor);
}


function aiQuery(args) {

    $.getJSON($SCRIPT_ROOT + '/apiImage', {

        image: args

    }, function (data) {

        document.getElementById('digitPre').textContent = "Recognized digit: " + data.result;

        console.log(data.result);

    });

    return false;
}

function DownloadImage23() {


    var canvasData = exportCanvas.toDataURL("image/png");

    $.ajax({
        url: 'test',
        type: 'POST',
        data: {
            data: canvasData
        }
    });
}


function DownloadImage() {
    var downloadData = exportCanvas.toDataURL("png");

    aiQuery(downloadData);
}


function DownloadImage2() {
    // const downloadName = document.getElementById("imageName").value;
    const downloadName = "one"

    const downloadData = exportCanvas.toDataURL("png");
    var download = document.createElement("a");
    download.href = downloadData;
    download.download = downloadName + ".png";
    download.click();
}

function SetErasing(value) {
    if (value) {
        erasing = true;
    }
    else {
        erasing = false;
    }
}

function Erase() {
    location.reload();
}

function SetTool(tool) {
    tools.brush = false;
    tools.eraser = false;
    tools.identifier = false;
    if (tool === "brush") {
        tools.brush = true;
    }
    else if (tool === "eraser") {
        tools.eraser = true;
    }
    else if (tool === "identifier") {
        tools.identifier = true;
    }
}

function IdentifyColor() {
    var drawX = Math.floor(mouse.x);
    var drawY = Math.floor(mouse.y);
    while (drawX % OFFSET != 0) {
        --drawX;
    }
    while (drawY % OFFSET != 0) {
        --drawY;
    }
    globalColor = colors[drawX / OFFSET][drawY / OFFSET];
    document.getElementById("colorPicker").value = globalColor;
}

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}