# Fridge Cam
This repo was for an IOT class project. 

We were tasked with creating an IOT system that solved a problem in our daily lives. We decided on a smart fridge camera
that will help keep track of the items in your fridge as well as provide a live view into your fridge so that you can check
what you have from anywhere via a mobile app.

The general flow is as follows:
1. Item is held in front of the Camera, photo is taken, item is classified using a CNN model.
2. Item photo and metadata is sent to the backend server.
3. Backend server processes the request and stores information in relevant resources.
4. Periodically, a photo is taken of the fridge and sent to the backend.
5. Every 5 minutes, temp and humidity is sent to the backend.
6. User opens swift IOS app and views what items are in the fridge, possibly requesting recipe suggestions.
7. Items flip to expired once their estimated expiration date passes.

We utilized AWS for our cloud infrastructure. The goal of the project was to build a cloud managed IOT system that had the foundations capable of scale. We could have done the entire project with just a local server on the LAN with the camera but personally I wanted to use this as an opportunity to enchance my cloud computing knowledge. Below is a rough diagram of our system. 
An EC2 instance acted as our central server providing an API interface for both the mobile app as well as the camera. This was written using Flask. All meta data surrounding the items in the fridge and the state of the fridge itself was stored in dynamoDB tables. All images of the items as they were put into the fridge along with fridge photos were stored in an S3 bucket. We used Twilio to send daily reminders of items expiring in the next few days. We also leveraged OpenAIs API to provide recipe suggestions based on the items expiring soon.


<p align="middle">
  <img src="/Assets/fridge_arch.png" width="400" height="400" style="margin-right: 20px;">
</p>

Here are some screenshots of swift mobile app.

<p align="middle">
  <img src="/Assets/home.png" width="200" height="400" style="margin-right: 20px;">
  <img src="/Assets/health.png" width="200" height="400" style="margin-left: 10px; margin-right: 10px;">
  <img src="/Assets/fridge.png" width="200" height="400" style="margin-left: 20px;">
</p>

