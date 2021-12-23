var express = require('express');
var router = express.Router();
var service = require('../controllers/service');
var path = require("path");
var fs = require('fs');
var app = express();
/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

// fetch the cal page.
router.get('/cal', function(req, res, next) {
  res.sendFile(path.join(app.get('views') + '/cal.html'));
});

//set(send) in keypoints from PI>
router.post('/setkeypoints', function(req, res, next) {

  service.updateClients(req.body)
  //console.log(JSON.stringify(req.body))  //for debug
  res.status(200).send("thankyou ")
});


module.exports = router;
