// modules =================================================
var bodyParser   = require('body-parser');
var express  = require('express');
var app      = express();

// configure app to let us get the data from a POST
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json({ type: 'application/vnd.api+json' })); 

// server static directory
app.use(express.static('public'));

// route to index
// app.get('/', function (req, res) {
//   res.send('Hello World!');
// });

// // accept POST request on the homepage
// app.post('/', function (req, res) {
//   res.send('Got a POST request');
// });
 app.post({
    type:"POST",
    beforeSend: function (request)
    {
      request.setRequestHeader('Content-Type', 'application/vnd.onem2m-res+json');
      request.setRequestHeader('X-M2M-Origin', '//localhost:10000');
      request.setRequestHeader('X-M2M-RI', '12345');
      request.setRequestHeader('Access-Control-Allow-Origin','*');
    },
    url: "http://localhost:8282/InCSE1/TestAE/PinContainer",
    data: {"m2m:cin":{"con":"fuckthisshit"}},
    dataType : 'json',   //you may use jsonp for cross origin request
    crossDomain:true,
    processData: false,
    success: function(msg) {
        console.log("The result =" + StringifyPretty(msg));
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
     alert(msg);
  }
  });

  // // send POST JSON Pin location to ODL datastore
  // var requestify = require('requestify'); 
  // requestify.get('http://apple.com').then(function(response) {
  //   // Get the response body (JSON parsed - JSON response or jQuery object in case of XML response)
  //   response.getBody();

  //   // Get the response raw body
  //   response.body;

  //   console.log(body);
  // });

// start up ===============================================

var server = app.listen(3000, function () {
  var host = server.address().address;
  var port = server.address().port;

  console.log('Snow plow app listening at http://%s:%s', host, port);
});


