const fs = require('fs');
var latestdatabucket = { "testdata" : "hello" }
var currentconfig = {};

var service = module.exports = {

    init: function()
    {
        let rawdata = fs.readFileSync('../config.json');
        currentconfig = JSON.parse(rawdata);
    },
    runchildproc: function()
    {
       // added test comment
        console.log("python path: " + process.env.SCOPE_PYTHON_PATH);
        console.log("script path: " + process.env.SCOPE_PYTHON_SCRIPT);
        var spawn = require('child_process').spawn
       // py = spawn('/home/pi/.virtualenvs/cv/bin/python', ['/home/pi/A_localGit/FlightScopeEyeball/golf_blob.py'],)
        py = spawn(process.env.SCOPE_PYTHON_PATH, [process.env.SCOPE_PYTHON_SCRIPT],)
        console.log("Started python process");

    },
     storeData: function(data)
     {
         latestdatabucket = data;
     },
     getCalData: function()
     {
         return latestdatabucket;
     },
     getConfig: function()
     {
         return currentconfig;
     },
     setConfig: function(data)
     {
         let stdata = JSON.stringify(data, null, 4);
         fs.writeFileSync('../config.json', stdata);
         currentconfig = data;
         return currentconfig;
     }
}