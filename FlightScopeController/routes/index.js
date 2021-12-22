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


router.get('/cal', function(req, res, next) {

  res.sendFile(path.join(app.get('views') + '/cal.html'));
});

router.post('/setkeypoints', function(req, res, next) {

 var bla = {};
 bla.hello = 0
  bla.a1 = [];
 bla.a1.push("myarray")

  service.updateClients(req.body)
  //console.log(JSON.stringify(req.body))
  res.status(200).send("thankyou ")
 // res.render('index', { title: 'Express' });
});


module.exports = router;
