from django import forms
from .models import Message, Category, Tag
from django_ckeditor_5.widgets import CKEditor5Widget


class MessageForm(forms.ModelForm):
    """消息创建和编辑表单"""
    content = forms.CharField(widget=CKEditor5Widget())
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Message
        fields = ['title', 'category', 'tags', 'content', 'image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置标签的查询集为空，在视图中根据需要填充
        self.fields['tags'].queryset = Tag.objects.all()