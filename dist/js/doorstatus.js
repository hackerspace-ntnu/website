var openString = "<span class='door-status'>Hackerspace er åpent. Velkommen inn! :)</span>";
var closedString = "<span class='door-status'>Hackerspace er dessverre ikke åpent nå. Sjekk igjen senere :)</span>";

var jqxhr = $.getJSON("api/door", console.log("door fetch success"));
jqxhr.done(console.log("door fetch second success"));
jqxhr.fail(console.log("door fetch error"));
jqxhr.always(console.log("door fetch complete"));

jqxhr.complete(function() {
    console.log( "door fetch second complete" );
    var doorstatusDiv = $("#door-status");
    if(jqxhr.responseJSON[0].isOpen) {
        doorstatusDiv.html(openString);
        doorstatusDiv.addClass('alert-success');
        doorstatusDiv.removeClass('alert-info');
    } else {
        doorstatusDiv.html(closedString);
    }
});