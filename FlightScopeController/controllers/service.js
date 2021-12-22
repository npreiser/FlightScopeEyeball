var WebSocket = require('ws');
var wss = new WebSocket.Server({ port: 22888 });

var wsclient = undefined;
wss.on('connection', function connection(ws) {
    wsclient = ws;
    // ws.on('message', function incoming(message) {
    //    console.log('received: %s', message);
    // });
    ws.on('close', function close() {
        console.log('client disconnected');
        wsclient = undefined;
    });
});

function dispatchData(data)
{
    if (wsclient != undefined)
        wsclient.send(JSON.stringify(data));
}

var service = module.exports = {

     updateClients: function(data)
     {
         dispatchData(data)
     }




}