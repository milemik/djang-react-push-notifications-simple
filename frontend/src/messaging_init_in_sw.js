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

requestPermission();