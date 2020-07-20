var request = require("request");
const fs = require('fs');
const path = require('path');
var http = require('http');

function getData() {
  return new Promise((res, rej) => {
    fs.readFile(path.join(__dirname, 'samples/newslaves.m4a'), 'base64', (err, resp) => {
      console.log(resp);
      var data = {
        'return': 'spotify',
        'api_token': '0295a1c0139a030849dd81359d92122a',
        'audio': resp,
      };

      request({
        uri: 'https://api.audd.io/',
        form: data,
        method: 'POST'
      }, function (err, resp, body) {
        let data = JSON.parse(body);

        res(data);
      });
    });
  })

}

http.createServer(function (req, res) {
  getData().then( d => {
    let c = JSON.stringify(d);
    console.log(c);
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write(`
    <h1>${d.result.title}</h1>
    <h2>${d.result.artist}</h2>
    <h2>${d.result.album}</h2>
    `);
    res.write(`
      <img width='200' height='200' src="${d.result.spotify.album.images[0].url}">
      <br>
      <p style='margin-top:200px;'>${c}</p>
    `);

    // res.write(c + '\n')
    res.end(); //end the response
  })
}).listen(8080); //the server object listens on port 8080