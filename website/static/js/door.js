/*
FILE NAME: js/door_status.js
WRITTEN BY: Jonas Hermansen Muribø
WHEN: November 2015
PURPOSE: reads the door-status of the hackerspace door
and returns the state(open/closed). loads and updates
the different bars that are responsive to this state
*/
​
//This script can only run on the same server as the actual door-script for the
//door to hackerspace (hackerspace.idi.ntnu.no/api/door), hence the placement at
//hackerspace.idi.ntnu.no/webtek/pages/
​
function checkDoor(){
	//Puts an iframe in the div with id="empty". Sets it to not display anything.
	document.getElementById("empty").innerHTML='<iframe type="text/html" style="display:none;" src="http://hackerspace.idi.ntnu.no/api/door" style=""></iframe>';
	//Upon loading the iframe, call the function below.
	document.getElementsByTagName("iframe")[0].addEventListener("load", function(){
		//A is the content of the iframe.
		var a = document.getElementsByTagName("iframe")[0];
		//B is the JSON-object one gets from parsing a.
		var b = JSON.parse(a.contentDocument.getElementsByTagName("pre")[0].innerHTML);
		//Debug
		console.log(b.isOpen.door);
		//Changes the logo-color and bar-color depending on wether the door is open or not.
		//On index.html the Hackerspace-picture is changed as well.
		if(b.isOpen.door){
			var status = document.getElementById("status");
			if(status != null) {
				document.getElementById("status").style.backgroundImage = "url('../img/Logo_green.png')";
			}
			document.getElementById("header").style.background = "#9cd590";
			document.getElementById("logo").style.backgroundImage = "url('../img/Logo_round_green.png')";
		} else {
			var status = document.getElementById("status");
			if(status != null) {
				document.getElementById("status").style.backgroundImage = "url('../img/Logo_white.png')";
			}
			document.getElementById("header").style.background = "#ea9989";
			document.getElementById("logo").style.backgroundImage = "url('../img/Logo_round_white.png')";
		}
	});
}
​
//Runs this code at page-load
addEventListener("load", checkDoor());
