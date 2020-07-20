let img;

function preload() {
  img = loadImage('mbdtf.png');
}

function setup() {
    createCanvas(200,200);
    background(51);
    img.resize(16, 16);
    img.loadPixels();

    let pix = img.pixels;
    let pixels = [];
    for (i = 0; i < pix.length; i += 4) {
        pixels.push([pix[i], pix[i+1], pix[i+2]]);
    }
    let str = '[';
    pixels.forEach(pixel => {
        str += `(${pixel[0]}, ${pixel[1]}, ${pixel[2]}),`
    })
    str = str.slice(0, -1);
    str += ']'
    console.log(str);
}