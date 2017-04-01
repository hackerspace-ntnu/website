from django import template

register = template.Library()


@register.inclusion_tag('inventory/cards/loan_detail.html', name='card_loan_detail')
def card_loan_detail(loan):
    return {'loan': loan}


@register.inclusion_tag('inventory/cards/item_detail.html', name='card_item_detail')
def card_item_detail(item, request, perms, loan=True, buttons=True):
    return {
        'item': item,
        'perms': perms,
        'request': request,
        'loan': loan,
        'buttons': buttons,
    }
