/**
 * Henter alle chips i tags-feltet i formen og setter det sammen til en string av id'er til tagsene
 */
function getChips() {
    var elements = document.getElementsByClassName('chip');
    var id_string = "";
    for (var i = 0; i < elements.length; i++) {
        id_string += elements[i].getAttribute('data-id') + " ";
    }
    // window.alert(id_string);
    return id_string;
}


$(".thumbnailPicker").click(function () {
    thumbWindow = window.open('/files/images');
});


function selectThumnail(src, id) {
    thumbWindow.close();
    $("input[name^=thumbnail]").val(id);
    $(".thumbnailPicker").find("div").css("background-image", "url(" + src + ")");
}
