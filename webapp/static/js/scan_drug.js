let detector = new window.BarcodeDetectionAPI.BarcodeDetector();
let interval;
let decoding = false;
let video = null;
let canvas = null;
let context = null;
let cameras = [];
let track;
let data_matrix_code = null;

const defaultZoom = 2;

function drawTarget() {
    const canvasWidth = canvas.width;
    const canvasHeight = canvas.height;

    const squareSize = 120; // Размер прицела
    const lineLength = 20;  // Длина линий на углах
    const lineWidth = 4;    // Толщина линий
    const color = "rgb(97, 218, 157)"; // Цвет прицела

    // Центрируем квадрат
    const x = (canvasWidth - squareSize) / 2;
    const y = (canvasHeight - squareSize) / 2;

    // Очистка канваса
    //ctx.clearRect(0, 0, canvasWidth, canvasHeight);

    // Рисуем полупрозрачный фон
    context.fillStyle = "rgba(0, 0, 0, 0.5)";
    //context.fillRect(0, 0, canvasWidth, canvasHeight);

    // Очищаем область внутри прицела
    context.fillStyle = "rgba(0, 0, 0, 0)";
    //context.fillRect(x, y, squareSize, squareSize);

    // Рисуем линии прицела
    context.strokeStyle = color;
    context.lineWidth = lineWidth;

    // Верхний левый угол
    context.beginPath();
    context.moveTo(x, y + lineLength);
    context.lineTo(x, y);
    context.lineTo(x + lineLength, y);
    context.stroke();

    // Верхний правый угол
    context.beginPath();
    context.moveTo(x + squareSize - lineLength, y);
    context.lineTo(x + squareSize, y);
    context.lineTo(x + squareSize, y + lineLength);
    context.stroke();

    // Нижний левый угол
    context.beginPath();
    context.moveTo(x, y + squareSize - lineLength);
    context.lineTo(x, y + squareSize);
    context.lineTo(x + lineLength, y + squareSize);
    context.stroke();

    // Нижний правый угол
    context.beginPath();
    context.moveTo(x + squareSize - lineLength, y + squareSize);
    context.lineTo(x + squareSize, y + squareSize);
    context.lineTo(x + squareSize, y + squareSize - lineLength);
    context.stroke();
}

function get_scanned_drug_data(dm_code) {
    $.ajax({
        type: 'POST',
        url: add_scanned_drug_url,
        data: {
            tg_user: tuser_id,
            dm: dm_code
        }
    }).done(function (drug_data) {
        initialize_add_scanned_drug_modal(drug_data);
    });
}

function test_request() {
    data_matrix_code = '010460180801341221myAUS4C56j9RU 91EE08 929NdpsBmbv+9t9+9E/TDNJHm9flmGrIe8AbZ6DYA3SQU='
    close_scan_drug_window();
}

async function detectAndDecode() {
    if (decoding) {
        return;
    }
    decoding = true;
    try {
        canvas.toBlob((blob) => {
            detector.detect(blob).then((res) => {
                if (res.length > 0) {
                    data_matrix_code = res[0]['rawValue'];
                    close_scan_drug_window();
                }
            });
        });
    } catch (error) {
        console.log(error);
    }
    decoding = false;
}

async function setZoom(value) {
    const constraints = {advanced: [{zoom: value}]};
    await track.applyConstraints(constraints);
}

async function listCameras() {
    let allDevices = await navigator.mediaDevices.enumerateDevices();
    cameras = [];
    for (let i = 0; i < allDevices.length; i++) {
        let device = allDevices[i];
        if (device.kind == 'videoinput') {
            cameras.push(device);
        }
    }
}

async function requestCameraPermission() {
    try {
        const constraints = {video: true, audio: false};
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        closeStream(stream);
    } catch (error) {
        console.log(error);
        throw error;
    }
}

function closeStream(stream) {
    if (stream) {
        const tracks = stream.getTracks();
        for (let i = 0; i < tracks.length; i++) {
            const track = tracks[i];
            track.stop();  // stop the opened tracks
        }
    }
    clearInterval(interval);
    decoding = false;
}

async function startCamera() {
    let selectedCamera = cameras[cameras.length - 1];
    const videoConstraints = {
        video: {
            deviceId: selectedCamera.deviceId,
            zoom: true
        },
        audio: false
    };
    try {
        const cameraStream = await navigator.mediaDevices.getUserMedia(videoConstraints);

        if (!video) {
            video = document.createElement('video');
            video.addEventListener('loadeddata', function () {
                video.play();
                setTimeout(videoLoop, 1000 / 30);
            });
        }
        video.srcObject = cameraStream;
        const videoTracks = video.srcObject.getVideoTracks();
        track = videoTracks[0];
        await setZoom(defaultZoom);

    } catch (error) {
        alert(error);
    }
}

async function videoLoop() {
    if (video && !video.paused && !video.ended) {
        let w = video.videoWidth;
        let h = video.videoHeight;

        const aspectRatio = w / h;
        const newHeight = canvas.width / aspectRatio;
        canvas.height = newHeight;

        context.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, canvas.width, canvas.height);
        drawTarget();
        await detectAndDecode();

        setTimeout(videoLoop, 1000 / 30);
    }
}

async function scanner_open_transition_end() {

}

function scanner_close_transition_end() {
    if (video) {
        video.pause();
        closeStream(video.srcObject);
        video = null;
    }
    if (data_matrix_code) {
        get_scanned_drug_data(data_matrix_code);
        data_matrix_code = null;
    }
    document.getElementById('control_scan_panel').style = 'background: rgba(0, 0, 0, 0%); top: -100%';
}

async function open_scan_drug_window() {
    await requestCameraPermission();
    await listCameras();
    await startCamera();

    document.getElementById('control_scan_panel').style = 'background: rgba(0, 0, 0, 30%); top: 0px';
    document.getElementById('dialogScanDrug').className = 'scanner_opened';

    const transition_opened = document.querySelector(".scanner_opened");
    transition_opened.removeEventListener('transitionend', scanner_close_transition_end);
    transition_opened.addEventListener('transitionend', scanner_open_transition_end);
}

function close_scan_drug_window() {
    document.getElementById('dialogScanDrug').className = 'scanner_closed';

    const transition_closed = document.querySelector(".scanner_closed");
    transition_closed.removeEventListener('transitionend', scanner_open_transition_end);
    transition_closed.addEventListener('transitionend', scanner_close_transition_end);
}

document.addEventListener('DOMContentLoaded', function () {
    canvas = document.getElementById("scanner_canvas");
    context = canvas.getContext("2d");
    video = document.getElementById("video");
});