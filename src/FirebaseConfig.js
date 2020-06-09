const firebase = require("firebase");
// Required for side-effects
require("firebase/firestore");

const firebaseConfig = {
    apiKey: "AIzaSyB6ht8hmslQpLppEHFIf2PzVLUoAgfixBU",
    authDomain: "domyresearch-25720.firebaseapp.com",
    databaseURL: "https://domyresearch-25720.firebaseio.com",
    projectId: "domyresearch-25720",
    storageBucket: "domyresearch-25720.appspot.com",
    messagingSenderId: "289203018353",
    appId: "1:289203018353:web:ca02f21563a640550319d0",
    measurementId: "G-WGYKJB490Q"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
//firebase.analytics();

var database = firebase.firestore();
var storage = firebase.storage();

module.exports = {
    database: database,
    storage: storage,
}
