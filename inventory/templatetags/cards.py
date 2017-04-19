from django import template

register = template.Library()


@register.inclusion_tag('inventory/cards/loan_detail.html', name='card_loan_detail')
def card_loan_detail(loan):
    return {'loan': loan}


@register.inclusion_tag('inventory/cards/item_detail.html', name='card_item_detail')
def card_item_detail(item, request, perms):
    return {
        'item': item,
        'perms': perms,
        'request': request,
    }


@register.inclusion_tag('inventory/cards/small_item_detail.html')
def small_card_item_detail(item, request, perms):
    return {
        'item': item,
        'perms': perms,
        'request': request,
    }


@register.inclusion_tag('inventory/cards/small_loan_detail.html')
def small_card_loan_detail(loan, date_description, date):
    return {
        'loan': loan,
        'date_description': date_description,
        'date': date
    }
