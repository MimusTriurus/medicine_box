let detector = new window.BarcodeDetectionAPI.BarcodeDetector();
let decoding = false;
let canvas = null;
let context = null;
let cameras = [];
let data_matrix_code = null;
let cameraEnhancer = null;
let cameraView = null;

const defaultZoom = 3;

function drawTarget() {
    const canvasWidth = canvas.width;
    const canvasHeight = canvas.height;

    const squareSize = 230; // Размер прицела
    const lineLength = 20;  // Длина линий на углах
    const lineWidth = 6;    // Толщина линий
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
                decoding = false;
            });
        });
    } catch (error) {
        console.error(error);
    }
}

async function startCamera() {
    if (cameraEnhancer === null) {
        cameraView = await Dynamsoft.DCE.CameraView.createInstance();
        cameraEnhancer = await Dynamsoft.DCE.CameraEnhancer.createInstance(cameraView);
        cameraEnhancer.setImageFetchInterval(1000 / 30);

        let strongKernel = cv.matFromArray(3, 3, cv.CV_32F, [
            -1, -1, -1,
            -1, 9, -1,
            -1, -1, -1
        ]);

        let dstImage = new cv.Mat();
        cameraEnhancer.on('frameAddedToBuffer', () => {
            let img = cameraEnhancer.getImage();
            let srcImage = cv.matFromArray(img.height, img.width, cv.CV_8UC4, img.bytes);
            cv.filter2D(srcImage, dstImage, cv.CV_8U, strongKernel);
            cv.imshow('scanner_canvas', dstImage);
            detectAndDecode();
            drawTarget();
            srcImage.delete();
        });
        cameras = await cameraEnhancer.getAllCameras();

        let selectedCamera = cameras[cameras.length - 1];
        const width = 640;
        const height = 480;

        await cameraEnhancer.selectCamera(selectedCamera);
        await cameraEnhancer.setResolution({width: width, height: height});
    }
    await cameraEnhancer.open(true);
    cameraEnhancer.startFetching();
    cameraEnhancer.setZoom({factor: parseFloat(defaultZoom)});
}

async function scanner_open_transition_end() {

}

function scanner_close_transition_end() {
    if (cameraEnhancer) {
        cameraEnhancer.stopFetching();
        //topic for discussion
        //cameraEnhancer.close();
    }
    if (data_matrix_code) {
        get_scanned_drug_data(data_matrix_code);
        data_matrix_code = null;
    }
    decoding = false;
    document.getElementById('control_scan_panel').style = 'background: rgba(0, 0, 0, 0%); top: -100%';
}

async function open_scan_drug_window() {
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
    canvas = document.getElementById('scanner_canvas');
    context = canvas.getContext('2d');
});