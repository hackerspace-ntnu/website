function showChildren(id) {
    // Viser og sjuler children av den taggen man checker/ unchecker.
    var parent = $('#' + id);
    var divClass = ".child-of-" + id;

    if (jQuery(parent).is(':checked')) {
        $(divClass).show('medium');
    }
    else {
        $(divClass).hide('medium');
        var childrenIDs = JSON.parse(jQuery(parent).attr('data-children-tags'));

        for (var i = 0; i < childrenIDs.length; i++) {
            $('#' + childrenIDs[i]).attr('checked', false);
            showChildren(childrenIDs[i]);  // To hide and uncheck grandchildren
        }
    }
}


function postCheckBoxes() {
    var obj = JSON.stringify(getCheckJSON(0, ""));
    $('#check_json').val(obj);
    $('#check-form').submit();
}


function getCheckJSON(parentTagID) {
    // Henter ut hvilke checkboxes som er valgt, og legger i en dict.
    var tagIDs;

    if (parentTagID == "") {
        var checkedBoxes = $('.tag-check-level-0:checked');
        var boxArray = [];
        for (var j = 0; j < checkedBoxes.length; j++) {
            boxArray.push(jQuery(checkedBoxes[j]).attr('id'));
        }
        tagIDs = boxArray;
    }
    else {
        tagIDs = JSON.parse($('#' + parentTagID).attr('data-children-tags'));
    }
    var returnJSON = {};

    for (var i = 0; i < tagIDs.length; i++) {
        var tagID = tagIDs[i];
        var checkElement = $('#' + tagID);
        var childChildren = JSON.parse(jQuery(checkElement).attr('data-children-tags'));
        if (jQuery(checkElement).is(':checked')) {

            if (childChildren.length > 0) {
                returnJSON[tagID] = getCheckJSON(tagID);
            }
            else {
                returnJSON[tagID] = {}
            }
        }
    }
    return returnJSON;
}
