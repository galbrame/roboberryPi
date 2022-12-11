/******************************************
* NAME: Megan Galbraith
* 
* REMARKS: The scripts run on the Raspberry Pi server
*
*******************************************/

var WEB_SERVER = "http://robopi.local:4000" //home LAN
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
*              observeable, as in the roboberry will not move/speed up as
*              expected.
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
* DESCRIPTION: Tell the roboberry to move or change direction
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
* DESCRIPTION: Sends a stop message to the roboberry
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
* DESCRIPTION: Collects the value of the speedometer radio buttons and updates
*              the roboberry's speed accordingly
******************************************/
function changeSpeed(speed) {
    // let speed = getRadioBtnValue();
    // let reqBody = "speed="+ speed;

    // myRequest = new XMLHttpRequest();
    // myRequest.addEventListener("load", POSTVerificationLoadEvent);
    // myRequest.open("POST", WEB_SERVER + "/api/stop");
    // myRequest.send(JSON.stringify(reqBody));
}
