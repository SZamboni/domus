# Domus Project
Project Domus is an attempt to create a generalize IOT devices server manager created by Simone Zamboni in the fist months of 2019.
It is called Domus from the latin home, because in domotics project normally you have a lot of different devices that you have to control in a centralize way.
The idea is simple: the server starts with no knowledge of the devices that will have to control and their functionalities, therefore the devices send a registration message to the server where they explain their functionalities, so that the server register the devices and it starts communicating with them, reading their state and sending to them commands.
The main component of this project is the server web developed using Django, and also some Arudino code hase been developed to check the viability of this implementation.

# Front-end

The user starts with a normal login:
![alt text](https://github.com/SZamboni/domus/blob/master/images/login.png)
Now the user can see his own categories, wich are a way of grouping devices:
![alt text](https://github.com/SZamboni/domus/blob/master/images/categories.png)
When a category is open the list of devices inside the category is showed:
![alt text](https://github.com/SZamboni/domus/blob/master/images/devices.png)
Every device has its own IP, port, path, its unique id and its type. The device type contains the information about the functionalities of the devices of that kind. The let's take a look at a single device:
![alt text](https://github.com/SZamboni/domus/blob/master/images/device.png)
There is a lot of going on here. In the center of the page you can see the three attributes of this device, att1, att2 and att3. Attributes represent the state of a device, if for example a device is a thermostat it can have the attribute "temperature" wich will tell the temperature readed by the device. Attributes can be booleans, (real) numbers and strings, and can be updated indipendently one from the other, in this page will be shown the most recent value arrived for each attribute.
On the bottom we can se a list of functions, let's click on the first:
![alt text](https://github.com/SZamboni/domus/blob/master/images/function.png)
Functions are commands that we can send to the device. Each function has a number of parameters that the user can set. Parameters are of three types, booleans, (real) numbers and strings, and there can be contraints on parameters, for example in the first parameter we can only choose between some predifined options and in the third parameter can be at maximum 50. The user set the parameter has he likes and then when the "Send Command" button is pressed an HTTP request is sent to the ip, port and path specified in the device information.
Let's now take a look at another functionality: alerts and notifications. In the device view if we click the "See Alerts" button we come to this view:
![alt text](https://github.com/SZamboni/domus/blob/master/images/alerts.png)
An alert is applied to an attribute of a device, when a new reading from the device with that attributes arrives the condition of the alert is checked (for example in this case we check if the attribute att1 is less than 20). If the check is true a notification is raised, you can see the number of unreaded notifications on the top right corner. Let's see the notification:
![alt text](https://github.com/SZamboni/domus/blob/master/images/notifications.png)
Here we can see the notification, to what alert it refers, wich value triggered the alert and when. We can also see unreaded notifications.
Let's say you have a thermostat, and you want to turn on the heaters when the temperature is less than 20 degrees. You put an alert on the temperature attribute of that device, and then you add to the alert a "FeedbackFunction", wich will send a command, like the one you can send with a function, automatically when the alert is triggered and the notification is created.
![alt text](https://github.com/SZamboni/domus/blob/master/images/feedbackFunction.png)
On this page you can create a FeedbackFunction for that alert.

# JSON Communication

Let's go more on a technical side, how a device can register themselve to the server?
With a POST request at the path /registerdevice/ with a JSON with a structure like:

![alt text](https://github.com/SZamboni/domus/blob/master/images/registrationJSON.png)

For this to work the device need to have three pieces of informations: the exact name of the owner, the username of the person that will control the device, the deviceID, unique between all the other devices registered in the server, and its deviceType, o when two devices of the same type register will have the same functionalities. Moreover the device need to know the server ip and port, so it can know where to send the request.
When the device has to send data to the server it will do it using a JSON like this:

![alt text](https://github.com/SZamboni/domus/blob/master/images/dataJSON.png)

And when the server will send commends to the device, like functions of FeedbackFunctions, it will do it using a JSON like this:

![alt text](https://github.com/SZamboni/domus/blob/master/images/commandJSON.png)

To test if this can work some code for Arduino (using the board Wemos D1 R2 for easier Wi-Fi access) has been developed. The code represent a dummy device that register itself on the server, that sends dummy data and that prints the command when it receives one.

# Repository Structure
In the "domus-django" folder is located the Django server that powers the entire solution. The main part of the code is in the "devices" folder.
In the "arduinoCode" folder is located the code tested using the board Wemos D1 R2 Arduino compatible that presents the main functionalities that a device should have in order to communicate with the server.

# Work assestment and future developments
This project was intended as a proof of concept for a general pourpouse IOT devices manager, and it served its pourpose. 
It has some bugs, a lot of functionalities can be added, the Arduino code can be refined and the UI is bad, but create a perfect and commercially viable product was never my intention.
I don't know if I will continue working on this idea, but sure it was fun, interesting, and it teached me a lot of stuff.
