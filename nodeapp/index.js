const express = require('express');
const fileUpload = require('express-fileupload');
const path = require('path');
const bodyparser = require('body-parser');
const fs = require('fs');
const app = express();
const pyshell = require('python-shell');

var exphbs  = require('express-handlebars');
var hbs = exphbs.create({ /* config */ });
app.engine('handlebars', hbs.engine);
app.set('view engine', 'handlebars');
 

app.use(fileUpload());
app.use(express.static('templates'));
//app.use(bodyparser({uploadDir:'/uploads'}));



app.post('/upload', function(req, res) {
  if (!req.files)
	return res.status(400).send('No files were uploaded.');
 
  
  let sampleFile = req.files.sampleFile;
  console.log(sampleFile);
 
  //always mp4, change if required
  var paths = path.join(__dirname, '/video/inputfile.mp4');
  console.log(paths);
  sampleFile.mv(paths, function(err) {
	   if(err){
			return res.status(500).send(err);
	   }
 
	   	//change this
		res.redirect('/uploaded');
		// else{
		// 	return res.status(200)
		// }
	
   });
});
// app.post('/upload', function (req, res) {

// 	console.log(req.files);
//     var tempPath = req.files.file.path,
//         targetPath = path.resolve('./images/image.png');
//     if (path.extname(req.files.file.name).toLowerCase() === '.jpg') {
//         fs.rename(tempPath, targetPath, function(err) {
//             if (err) throw err;
//             console.log("Upload completed!");
//         });
//     } else {
//         fs.unlink(tempPath, function () {
//             if (err) throw err;
//             console.error("Only .jpg files are allowed!");
//         });
//     }
//     // ...
// });

app.get('', function(req, res){
	
	// pyshell.run('test.py', function (err, result) {
	// 	if (err) throw err;
	// 	console.log('finished' + result);
	// });

	res.render('home');
});

// app.get('/img', function(req, res){

// 	res.sendfile(path.resolve('./images/filename.jpg'));
// });
app.get('/uploaded', function(req, res){

	res.render('uploaded');

});

app.listen(8000);