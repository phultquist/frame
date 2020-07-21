const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
let l = parseInt(urlParams.get('n')) || 16;
console.log(l);
let input, button

let img;
let imgname = 'mbdtf.png'

function preload() {
    img = loadImage(imgname);
}

function setup() {

    input = createInput();
    // createP('pixels across')
    button = createButton('set');
    button.mousePressed(() => {
        if (isNaN(input.value())) {
            alert("that's not a number")
        } else if (input.value() > 150) {
            alert('why')
        } else {
            window.location = 'https://phultquist.github.io/smart-album-cover/?n=' + input.value();
        }
    });

    createCanvas(24 * 24, 24 * 24);
    img.resize(l, l);
    img.loadPixels();

    let pix = img.pixels;
    let pixels = [];
    let correctRed = false;
    for (i = 0; i < pix.length; i += 4) {
        if (pix[i] < 255 && pix[i] > 230 && correctRed) {
            pixels.push([255,0,0]);
        } else {
            pixels.push([pix[i], pix[i + 1], pix[i + 2]]);
        }
    }

    let grouped = [];
    for (j = 0; j < pixels.length; j += l) {
        let group = []
        for (k = 0; k < l; k++) {
            group.push(pixels[j + k])
        }
        grouped.push(group);
    }

    let structured = [];
    grouped.forEach((group, i) => {
        if (i % 2 == 1) {
            group = group.reverse();
        }
        group.forEach(pixel => {
            structured.push(pixel);
        })
    })

    drawGrid(structured)

    let str = '[';

    structured.forEach(pixel => {
        str += `(${pixel[0]}, ${pixel[1]}, ${pixel[2]}),`
    })
    str = str.slice(0, -1);
    str += ']'
    console.log(str);
}

function drawGrid(pixels) {
    for (i in pixels) {
        let x = i % l,
            y = Math.floor(i / l);
        if (y % 2 == 1) {
            x = l - 1 - x;
        }
        fill(pixels[i][0], pixels[i][1], pixels[i][2])

        let pwidth = Math.sqrt(width) * Math.sqrt(width) / l
        rect(x * pwidth, y * pwidth, pwidth, pwidth);
    }
}