firebase.auth().signInAnonymously();

// const firebase = require("firebase");
// // Required for side-effects
// require("firebase/firestore");

// firebase.initializeApp({
//   apiKey: 'AIzaSyCtouf5l5UDbda3KXt9CWOAiF4GtsDqoo8',
//   authDomain: 'calialert.firebaseapp.com',
//   projectId: 'calialert'
// });

var db = firebase.firestore();

/*document.getElementById("lol").addEventListener("click",
function getData (e) {
  e.preventDefault();
  let xd = document.getElementById('xd');
  console.log(xd);
  let formData = new FormData(xd);
  var xhr = new XMLHttpRequest();
  xhr.open("POST", '/insertData', true);
  xhr.send(formData);

  for(let x of formData.values()){
    console.log(x);
  }
});*/
const inputPhoneNumber = document.querySelector("#number");
const inputZipCode = document.querySelector("#zip");
const saveButton = document.querySelector("#saveButton");

saveButton.addEventListener("click", function() {
    const docRef = db.collection("users").doc();
    const number = inputPhoneNumber.value;
    const zip = inputZipCode.value;
    docRef.set({
        phoneNumber: number, zip
    }).then(function() {
        console.log("Number added!");
    }).catch(function (error){
        console.log("Got an error: ", error);
    });
});
