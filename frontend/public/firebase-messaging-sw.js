 // Scripts for firebase and firebase messaging
 importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");
 importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js");

 // Initialize the Firebase app in the service worker by passing the generated config
const firebaseConfig = {
    apiKey: "AIzaSyDTx8SGRHbE00njG_RfOIP6n0ZENEVzLmQ",
    authDomain: "mytestproject-9b39f.firebaseapp.com",
    projectId: "mytestproject-9b39f",
    storageBucket: "mytestproject-9b39f.appspot.com",
    messagingSenderId: "363755251159",
    appId: "1:363755251159:web:69b6fa8b98258681281792"
};
 firebase.initializeApp(firebaseConfig);

 // Retrieve firebase messaging
 const messaging = firebase.messaging();

 messaging.onBackgroundMessage(function(payload) {
   console.log("Received background message ", payload);

   const notificationTitle = payload.notification.title;
   const notificationOptions = {
     body: payload.notification.body,
   };

   self.registration.showNotification(notificationTitle, notificationOptions);
 });