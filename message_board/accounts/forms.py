from django import forms
from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    """用户资料更新表单"""
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }