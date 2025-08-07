from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin
from django import forms
from .models import *



class CustomGroupForm(forms.ModelForm):
    user_set = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple('Users', is_stacked=False)
    )

    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['user_set'].initial = self.instance.user_set.all()

    def save(self, commit=True):
        group = super().save(commit)
        if commit:
            group.user_set.set(self.cleaned_data['user_set'])
        return group

class GroupAdminWithUsers(GroupAdmin):
    form = CustomGroupForm
    filter_horizontal = ('permissions',)


admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Profile)
admin.site.register(Borrow)

admin.site.unregister(Group)
admin.site.register(Group, GroupAdminWithUsers)
