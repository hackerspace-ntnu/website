from django import forms

from .models import Profile, DutyTime, Skill


class ProfileForm(forms.Form):
    pass
#    study = forms.CharField(label='Studieretning', max_length=100)
#    access_card = forms.CharField(label='Adgangskort', max_length=100)
#    image = forms.ImageField(label='Profilbilde')
#
#    duty = forms.ModelMultipleChoiceField(DutyTime.objects.all)
#    skills = forms.ModelMultipleChoiceField(Skill.objects.all)



class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'duty', 'auto_duty', 'skills', 'study', 'access_card']
        labels = {
                'image': "Profilbilde",
                'duty': "Vakttid",
                'auto_duty': "Hent vakt(er) automatisk",
                'skills': "Ferdigheter",
                'study': "Studieprogram",
                'access_card': "Adgangskort",
            }

class NameSearchForm(forms.Form):
   name = forms.CharField(max_length=200)
