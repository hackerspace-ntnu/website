function addItem() {
    var nameChips = $('.ac-users .chip');
    if (nameChips.length > 0) {
        var nameChip = nameChips[0];

        var name = jQuery(nameChip).attr('data-text');
        var id = jQuery(nameChip).attr('data-id');
        var quantity = $('input#quantity-field').val();

        addChip(name, id, quantity);

    }
}

function addChip(name, id, quantity) {
    if (quantity > 0) {
        var existing = $('#chosen-' + id);
        if (jQuery(existing).length) {
            existing.html(quantity + " " + name + '<i class="close material-icons">close</i>');
            existing.attr('data-quantity', quantity);
        }
        else {
            var chip = '<div class="chip chosen-item-chips" data-quantity="' + quantity +
                '" id="chosen-' + id + '" data-id="' + id + '">' + quantity + " " + name +
                ' <i class="close material-icons">close</i> </div>  ';
            $('.chosen-items-chips').append(chip);
        }
    }
    else {
        // TODO feilmelding, man må skrive inn et antall.
    }
}
