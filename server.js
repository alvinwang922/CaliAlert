const express = require('express');
const firebase = require('firebase');
const http = require('http');
const bodyParser = require('body-parser');
const app = express();
const server = http.createServer(app);
firebase.auth().signInAnonymously();

const port = process.env.PORT || 3001;
server.listen(port, '0.0.0.0', () => {
    console.log(`Server listening on port ${port}`);
});

const phoneNumbers = [];
const names = [];
const areaCodes =[];

const firebaseConfig = {
  apiKey: "AIzaSyCtouf5l5UDbda3KXt9CWOAiF4GtsDqoo8",
  authDomain: "calialert.firebaseapp.com",
  databaseURL: "https://calialert.firebaseio.com",
  projectId: "calialert",
  storageBucket: "calialert.appspot.com",
  messagingSenderId: "291762742438",
  appId: "1:291762742438:web:6334f6baccf1788d658067",
  measurementId: "G-VQQT76C881"
};

const admin = require('firebase-admin');

let serviceAccount = require('serviceAccountKey.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

let db = admin.firestore();

app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', (req, res) => {
    res.sendFile(__dirname + "/public/index.html");
});

app.post('/insertData', (req, res) => {

    const keywords = req.query.keywords;
    for (let i = 0; i < phoneNumbers.length; i++) {
        if (phoneNumbers[i]["number"].includes(number)) {
            break;
        }
        else {
          var array = {"name": params.name, "number": params.number};
        }
    }

    phoneNumbers.push(array);

    console.log(JSON.stringify(phoneNumbers));
    //fs.writeFile("PhoneNumbers.json", JSON.stringify(phoneNumbers), function(err) {
    if (err) {
        console.log(err);
    }
    });
    res.redirect('/');
});

app.get('/getData', (req, res) => {
    res.send(phoneNumbers.toString());
});
