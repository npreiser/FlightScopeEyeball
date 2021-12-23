


function init()
{
    ws = new WebSocket("ws://192.168.1.73:22888/");

        ws.onopen = function() {

            console.log("ws is open !!!")
        };

        ws.onmessage = function (evt) {    // handler for socket
            var dataobj = JSON.parse(evt.data);
            buildTable(dataobj)
        };

        ws.onclose = function() {
            // websocket is closed.
            // alert("Connection is closed...");
        };
}

function buildTable(mydata)
{

    // EXTRACT VALUE FOR HTML HEADER.
    var col = [];
    for (var i = 0; i < mydata.length; i++) {
        for (var key in mydata[i]) {
            if (col.indexOf(key) === -1) {
                col.push(key);
            }
        }
    }
    // CREATE DYNAMIC TABLE.
    var table = document.createElement("table");

    // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

    var tr = table.insertRow(-1);                   // TABLE ROW.

    for (var i = 0; i < col.length; i++) {
        var th = document.createElement("th");      // TABLE HEADER.
        th.innerHTML = col[i];
        tr.appendChild(th);
    }

    // ADD JSON DATA TO THE TABLE AS ROWS.
    for (var i = 0; i < mydata.length; i++) {

        tr = table.insertRow(-1);

        for (var j = 0; j < col.length; j++) {
            var tabCell = tr.insertCell(-1);
            tabCell.innerHTML = mydata[i][col[j]];
        }
    }

    // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
    var divContainer = document.getElementById("tableholder");
    divContainer.innerHTML = "";
    divContainer.appendChild(table);

}
