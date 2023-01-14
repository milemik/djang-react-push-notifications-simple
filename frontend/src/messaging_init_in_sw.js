import { initializeApp } from "firebase/app";
import { getMessaging, getToken } from "firebase/messaging";

const firebaseConfig = {
    apiKey: "AIzaSyDTx8SGRHbE00njG_RfOIP6n0ZENEVzLmQ",
    authDomain: "mytestproject-9b39f.firebaseapp.com",
    projectId: "mytestproject-9b39f",
    storageBucket: "mytestproject-9b39f.appspot.com",
    messagingSenderId: "363755251159",
    appId: "1:363755251159:web:69b6fa8b98258681281792"
};

function requestPermission() {
    console.log("Requesting permission...");
    Notification.requestPermission().then((permission) => {
        if (permission === "granted") {
            console.log("Notification permission granted.");
            const app = initializeApp(firebaseConfig);

            const messaging = getMessaging(app);
            getToken(messaging, {
                vapidKey:
                    "BC7HBEUsioUTzjSKeifDTWVvz6y_5RpYy1Z5ArJLdGZ71UZC6DvWsiVnD-q1ZlqZeMr57aE9EPZ0pDCvShVbhHE",
            }).then((currentToken) => {
                if (currentToken) {
                    postData('http://localhost:8000/add_device/', { push_uid: currentToken })
                        .then((data) => {
                            console.log(data); // JSON data parsed by `data.json()` call
                        });
                    console.log("currentToken: ", currentToken);
                } else {
                    console.log("Can not get token");
                }
            });
        } else {
            console.log("Do not have permission!");
        }
    });
}


async function postData(url = '', data = {}) {
    // Default options are marked with *
    console.log("Sending data to backend............")
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, cors, same-origin
        // credentials: 'include', // include, *same-origin, omit
        headers: {
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    if (response.statusCode !== 200) {
        return null
    }
    return response.json(); // parses JSON response into native JavaScript objects
}

requestPermission();