let img;

function preload() {
    img = loadImage('mbdtf.png');
}

function setup() {
    createCanvas(200, 200);
    background(51);
    img.resize(16, 16);
    img.loadPixels();

    let pix = img.pixels;
    let pixels = [];
    for (i = 0; i < pix.length; i += 4) {
        pixels.push([pix[i], pix[i + 1], pix[i + 2]]);
    }

    let grouped = [];
    for (j = 0; j < pixels.length; j += 16) {
        let group = []
        for (k = 0; k < 16; k++) {
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

    let str = '[';

    structured.forEach(pixel => {
        str += `(${pixel[0]}, ${pixel[1]}, ${pixel[2]}),`
    })
    str = str.slice(0, -1);
    str += ']'
    console.log(str);
}