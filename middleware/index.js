const express = require('express')
const bodyParser = require('body-parser');
const app = express()
const fs = require('fs');
const Json2csvParser = require('json2csv').Parser;
const fields = [
    {
        label: 'Title',
        value: 'title'
    },
    {
        label: 'URL',
        value: 'url'
    }
];
const request = require('request');
app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', function (req, res) {
    res.render("index", { query: null })
})

app.post('/', function (req, res) {
    let squery = req.body.search
    request.post({ url: "http://localhost:5000",json:true, form: { query: squery } }, function (err, pres, body) {
        if (err) {
            res.render('index', { query: squery });
            console.log(err)
        } else {
            const parser = new Json2csvParser({ fields });
            const csv = parser.parse(body);
            var headers = {
                'Content-type': 'application/octet-stream',
                'Content-Disposition': 'attachment; filename=result.csv'
            };
            res.writeHead(200, headers);
            res.end(csv);
        }
    })

})

app.listen(3000, function () {
    console.log('G2CSV listening on port 3000')
})
