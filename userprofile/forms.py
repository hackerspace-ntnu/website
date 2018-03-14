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



class ProfileModelFormUser(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'study']
        labels = {
                'image': "Profilbilde",
                'study': "Studieprogram",
            }

class ProfileModelFormMember(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'group', 'duty', 'auto_duty', 'skills', 'study', 'access_card']
        labels = {
                'image': "Profilbilde",
                'duty': "Vakttid",
                'group': "Grupper",
                'auto_duty': "Hent vakt(er) automatisk",
                'skills': "Ferdigheter",
                'study': "Studieprogram",
                'access_card': "Adgangskort",
            }
        
class ProfileModelFormAdmin(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'name', 'auto_name', 'group', 'duty', 'auto_duty', 'skills', 'study', 'access_card']
        labels = {
                'image': "Profilbilde",
                'name': "Navn",
                'auto_name': "Hent navn fra bruker",
                'group': "Gruppe",
                'duty': "Vakttid",
                'auto_duty': "Hent vakt(er) automatisk",
                'skills': "Ferdigheter",
                'study': "Studieprogram",
                'access_card': "Adgangskort",
            }

class NameSearchForm(forms.Form):
   name = forms.CharField(max_length=200)
