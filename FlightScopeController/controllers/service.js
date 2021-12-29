//var WebSocket = require('ws');
//var wss = new WebSocket.Server({ port: 22888 });

//var wsclient = undefined;

var latestdatabucket = undefined
/*wss.on('connection', function connection(ws) {
    wsclient = ws;
    // ws.on('message', function incoming(message) {
    //    console.log('received: %s', message);
    // });
    ws.on('close', function close() {
        console.log('client disconnected');
        wsclient = undefined;
    });
});  */


function dispatchData(data)
{
    if (wsclient != undefined)
        wsclient.send(JSON.stringify(data));
}

var service = module.exports = {

    runchildproc: function()
    {
        console.log("python path: " + process.env.SCOPE_PYTHON_PATH);
        console.log("script path: " + process.env.SCOPE_PYTHON_SCRIPT);
        var spawn = require('child_process').spawn
       // py = spawn('/home/pi/.virtualenvs/cv/bin/python', ['/home/pi/A_localGit/FlightScopeEyeball/golf_blob.py'],)
        py = spawn(process.env.SCOPE_PYTHON_PATH, [process.env.SCOPE_PYTHON_SCRIPT],)
        console.log("Started python process");

    },
     updateClients: function(data)
     {
         dispatchData(data) // send data out to the client web pages that are currently on (via web socket)
     },
     storeData: function(data)
     {
         latestdatabucket = data;
     },
     getCalData: function()
     {
         return latestdatabucket;
     }
}