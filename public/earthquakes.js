const firebase = require('firebase');
const admin = require('firebase-admin');

let serviceAccount = require('serviceAccountKey.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

let db = admin.firestore();

var items = [];
var dict;

function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}

$.ajaxSetup({
  async: false
});

$.getJSON('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2020-01-31&maxlatitude=42.010122&minlatitude=32.467133&maxlongitude=-113.881617&minlongitude=-124.718872&minmagnitude=2', function (data) {

  $.each(data.features, function (key, val) {
    dict = {
      "title": val.properties.title,
      "coords": val.geometry.coordinates,
      "mag": val.properties.mag,
      "id": val.id
    }
    items.push(dict);

  });
});

items.forEach(element =>

  $.getJSON('https://us1.locationiq.com/v1/reverse.php?key=pk.8f9961f595035136176ee020eb95c961' + '&lat=' + element["coords"][1] + '&lon=' + element["coords"][0] + '&format=json', function (x) {
    element["county"] = x.address.county;
    sleep(1001);
  })
)

var setDoc;

items.forEach(element => 
  setDoc = db.collection('earthquakes').doc(element["id"]).set(
    {
      "title": element["title"],
      "coords": element["coords"],
      "mag": element["mag"]
    })
);


