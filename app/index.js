const express = require('express')
const bodyParser = require('body-parser');
const app = express()
app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true}));

app.get('/', function (req, res) {
    res.render("index")
})

app.post('/', function (req, res) {
    res.render('index');
})

app.listen(3000, function () {
    console.log('G2CSV listening on port 3000')
})