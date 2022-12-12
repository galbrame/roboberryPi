/******************************************
* NAME: Megan Galbraith
* 
* REMARKS: The front-end scripts for the roboberry control web page. Because
*          the roboberry has been running both on my home LAN (easily discoverable)
*          and my university LAN, I have two versions of WEB_SERVER to toggle on/off
*          as needed. Serving up and access resources on a local domain avoids any
*          annoying cross-origin domain (CORS) issues if I were to host from my 
*          personal webpage or something.
*
*******************************************/

//regular server operates on port 5000, test server expected on port 4000
var WEB_SERVER = "http://robopi.local:5000" //home LAN
//var WEB_SERVER = "140.193.105.207:5000" //um-secure IP
var myRequest; //XHR request


/******************************************
* getRadioBtnValue
*
* DESCRIPTION: Gets the currently checked radio button value
* 
* RETURNS:
*       val: the value stored in the checked radio button (ie, speed)
******************************************/
function getRadioBtnValue() {
    let radioGrp = document.getElementsByName("speed");
    let val = 0;

    for (let i = 0; i < radioGrp.length; i++) {
        if (radioGrp[i].checked) {
            val = Number(radioGrp[i].value);
        }
    }

    return val;
}


/******************************************
* POSTVerificationLoadEvent
*
* DESCRIPTION: Used to log errors, as valid responses should be real-time
*              observeable (ie, the roboberry will not move/speed up as
*              expected but we liekly won't know why).
******************************************/
function POSTVerificationLoadEvent() {
    if (myRequest.status != 200) {
        console.log("A error occured:");
        console.log(myRequest.responseText);
    }
}


/******************************************
* moveCar
*
* DESCRIPTION: Sends a request to change the direction of (or stop) the
*              roboberry, based on whichever button the user selected.
*              speed data is also collected from the radio button group in
*              case it has been updated since the last time the roboberry
*              moved.
* 
* PARAMETERS:
*       direction: the direction to move the roboberry
******************************************/
function moveCar(direction) {
    let speed = getRadioBtnValue();
    let reqBody = "direction=" + direction + "\nspeed="+ speed;
    
    myRequest = new XMLHttpRequest();
    myRequest.addEventListener("load", POSTVerificationLoadEvent);
    myRequest.open("POST", WEB_SERVER + "/api/move");
    myRequest.send(JSON.stringify(reqBody));
}


/******************************************
* stopCar
*
* DESCRIPTION: Sends a stop message to the roboberry. Does not have a
*              request body (0's are assumed for all states).
******************************************/
function stopCar() {
    myRequest = new XMLHttpRequest();
    myRequest.addEventListener("load", POSTVerificationLoadEvent);
    myRequest.open("POST", WEB_SERVER + "/api/stop");
    myRequest.send();
}


/******************************************
* changeSpeed
*
* DESCRIPTION: Sends a request to change the speed of the roboberry. Sends
*              the desired speed (a PWM value) in a request. Side note: PMW
*              values can be between 0 to 1024, with 512 representing a 50%
*              duty cycle for the motor. 
*
* PARAMETERS:
*       speed: the user selected speed for the roboberry
******************************************/
function changeSpeed(speed) {
    let reqBody = "speed=" + speed;

    myRequest = new XMLHttpRequest();
    myRequest.addEventListener("load", POSTVerificationLoadEvent);
    myRequest.open("POST", WEB_SERVER + "/api/speed");
    myRequest.send(JSON.stringify(reqBody));
}


/******************************************
* toggleLight
*
* DESCRIPTION: Turn the LED off or on.
******************************************/
function toggleLight() {
    let toggle = document.getElementById("light_switch");
    let val = "0"; //default is light off

    //if light is off, turn it on
    if (toggle.checked) {
        val = "1";
    }

    let reqBody = "light=" + val;

    myRequest = new XMLHttpRequest();
    myRequest.addEventListener("load", POSTVerificationLoadEvent);
    myRequest.open("POST", WEB_SERVER + "/api/light");
    myRequest.send(JSON.stringify(reqBody));
}