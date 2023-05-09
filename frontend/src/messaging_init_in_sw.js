import { initializeApp } from "firebase/app";
import { getMessaging, getToken } from "firebase/messaging";

console.log(process.env.REACT_APP_FB_API_KEY);

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FB_API_KEY,
  authDomain: `${process.env.REACT_APP_FB_PROJECT_ID}.firebaseapp.com`,
  projectId: process.env.REACT_APP_FB_PROJECT_ID,
  storageBucket: `${process.env.REACT_APP_FB_PROJECT_ID}.appspot.com`,
  messagingSenderId: process.env.REACT_APP_FB_SENDER_ID,
  appId: process.env.REACT_APP_FB_APP_ID,
  measurementId: process.env.REACT_APP_FB_MANAGEMENT_ID,
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
                    "BBGHDrt4NKEqZRYRkdRXjeGrcjxMbBt3kMDw0W0eRW-1AV5kga73-EODnRy8c-jurTz2YJUlvzWcVo9__tydfHo",
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