from django.contrib import admin
from .forms import AssetForm, LoanForm
from .models import Asset, Loan, Place, Shelf
from django.contrib.admin.filters import SimpleListFilter


class NullFilterSpec(SimpleListFilter):
    title = u'Available'

    parameter_name = u'loan'

    def lookups(self, request, model_admin):
        return (
            ('0', ('Yes'),),
            ('1', ('No'),),
        )

    def queryset(self, request, queryset):
        kwargs = {
            '%s' % self.parameter_name: None,
        }
        if self.value() == '0':
            return queryset.filter(**kwargs)
        if self.value() == '1':
            return queryset.exclude(**kwargs)
        return queryset


class LoanAdmin(admin.ModelAdmin):
    def get_form(self, request, *args, **kwargs):
        form = super(LoanAdmin, self).get_form(request, *args, **kwargs)
        form.base_fields['lender'].initial = request.user.username
        return form
    list_display = ('id', 'user', 'from_date', 'to_date', 'returned')
    search_fields = ['id', 'user__username']
    list_filter = ['returned']
    autocomplete_fields = ['user']
    model = Loan
    form = LoanForm


class AssetAdmin(admin.ModelAdmin):
    list_filter = [NullFilterSpec]
    model = Asset
    form = AssetForm

admin.site.register(Loan, LoanAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(Place)
admin.site.register(Shelf)