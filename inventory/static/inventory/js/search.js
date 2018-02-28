// TODO gjør denne funksjonaliteten utilgjengelig for andre brukere som ikke er logget inn


function listElement(item) {
    var info = item.split("_");
    var item_id = item[0];
    var name = info[1];
    // TODO evt gjøre hvert element til en chip, og legge til et kryss for å fjerne, checkbox blir for mye
    return '<li><div id="' + item_id + '"><p>' + name + '</p></div><li>'
}

function getCheckedIds() {
    var elements = $('input:checked');
    var elements_string = "";
    for (var i = 0; i < elements.length; i++) {
        elements_string += elements[i].getAttribute('id') + '_';
    }
    return elements_string;
}

function update() {

    var elements = $('input:checked');

    // nullstille info i sidemenyen
    $('#hei').html("");
    $('div.left-list ul').html("");

    var submit_button = $('#change_multiple');
    submit_button.html("");
    submit_button.hide();

    if (elements.length > 0) {
        $('div p#hei').html("<b>Merkede Elementer</b>");
        submit_button.html("Endre");
        submit_button.show();
    }

    for (var i = 0; i < elements.length; i++) {

        var name = elements[i].getAttribute('id');
        name += "_" + elements[i].getAttribute('name');
        $('div ul#merkede-elementer').append(listElement(name))
    }

}

// TODO prøver å få funksjonen i add_item.js til å fungere, kan da fjerne denne
function postItems() {
    $('#items-for-changing').val(getCheckedIds());
    $('#multiple_items_form').submit();
}
