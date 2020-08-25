const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
let l = parseInt(urlParams.get('n')) || 16;
console.log(l);
let input, button

let img, cimg;

//xxx
// let imgname = 'https://i.scdn.co/image/ab67616d00004851806c160566580d6335d1f16c'

//graduation
let imgname = 'https://i.scdn.co/image/ab67616d000048519bbd79106e510d13a9a5ec33'

//young dumb and broke
// let imgname = 'https://i.scdn.co/image/ab67616d00004851988ede5e1276e758b5f9e577'

//runaway
// let imgname = 'https://i.scdn.co/image/ab67616d00004851d9194aa18fa4c9362b47464f'

function preload() {
    img = loadImage(imgname);
    cimg = loadImage(imgname)
}

function setup() {
    createCanvas(830, 400);

    img.resize(l, l);
    img.loadPixels();

    let pix = img.pixels;
    let pixels = [];
    let correctRed = false;
    for (i = 0; i < pix.length; i += 4) {
        if (pix[i] < 255 && pix[i] > 230 && correctRed) {
            pixels.push([255, 0, 0]);
        } else {
            pixels.push([pix[i], pix[i + 1], pix[i + 2]]);
        }
    }


    let grouped = groupPixels(pixels)
    // console.log(grouped);
    let structured = structure(grouped)

    drawGrid(structured, 0, false)
    // return






    cimg.loadPixels()

    let raw = cimg.pixels;
    let org = []
    let cpix = [];

    for (i = 0; i < raw.length; i += 4) {
        org.push([raw[i], raw[i + 1], raw[i + 2]]);
    }

    org = groupPixels(org);
    console.log(org);
    let stepsize = cimg.width / l;
    console.log(stepsize);
    for (x = 0; x < org.length; x += stepsize) {
        let row = org[x]
        let smallrow = []
        for (y = 0; y < row.length; y += stepsize) {
            let toAvg = []
            for (a = 0; a < stepsize; a++) {
                for (b = 0; b < stepsize; b++){
                    toAvg.push(org[x+a][y+b])
                }
            }
            // let avg = averagePixels([org[x][y], org[x][y +1], org[x+1][y], org[x+1][y+1]])
            let avg = generalize(toAvg)
            smallrow.push(avg);
        }
        cpix.push(smallrow);
    }

    let rawStructured = structure(cpix)
    drawGrid(rawStructured, width / 2 + 10, false)
}

function drawGrid(pixels, offset, snake) {
    noStroke();
    let len = height
    for (i in pixels) {
        let x = i % l,
            y = Math.floor(i / l);
        if (y % 2 == 1 && snake) {
            x = l - 1 - x;
        }
        fill(pixels[i][0], pixels[i][1], pixels[i][2])

        let pwidth = Math.sqrt(len) * Math.sqrt(len) / l
        rect(offset + x * pwidth, y * pwidth, pwidth, pwidth);
    }
}

function structure(grouped) {
    let structured = [];
    grouped.forEach((group, i) => {
        if (i % 2 == 1) {
            // group = group.reverse();
        }
        group.forEach(pixel => {
            structured.push(pixel);
        })
    })

    return structured;
}

function groupPixels(pixels) {
    let sq = Math.sqrt(pixels.length)
    console.log(sq);
    let grouped = [];
    for (j = 0; j < pixels.length; j += sq) {
        let group = []
        for (k = 0; k < sq; k++) {
            group.push(pixels[j + k])
        }
        grouped.push(group);
    }
    return grouped
}


function generalize(pi) {
    let s = 0
    let totals = [s*pi.length,s*pi.length,s*pi.length]
    let component;
    pi.forEach(pixel => {
        for (n = 0; n < totals.length; n++) {
            component = pixel[n]
            // if (component > 200) component = 255 
            totals[n] += component
        }
    })
    return totals.map(t => t / pi.length)
}