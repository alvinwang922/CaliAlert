const express = require('express');
const http = require('http');
const bodyParser = require('body-parser');
const app = express();
const server = http.createServer(app);

const port = process.env.PORT || 3001;
server.listen(port, '0.0.0.0', () => {
    console.log(`Server listening on port ${port}`);
});

const phoneNumbers = [];

app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', (req, res) => {
    res.sendFile(__dirname + "/public/index.html");
});

app.post('/insertData', (req, res) => {
    const params = req.body;
    phoneNumbers.push(params.flavor);
    res.redirect('/');
});

app.get('/getData', (req, res) => {
    res.send(phoneNumbers.toString());
});

app.get('/count', (req, res) => {
    const flavor = req.query.flavor;
    let count = 0;
    for (let i = 0; i < phoneNumbers.length; i++) {
        if (phoneNumbers[i] == flavor) {
            count++;
        }
    }
    res.send(count.toString());
});
