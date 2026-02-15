from django import forms
from .models import Message, Tag
from django_ckeditor_5.widgets import CKEditor5Widget


class MessageForm(forms.ModelForm):
    """消息创建和编辑表单"""
    content = forms.CharField(widget=CKEditor5Widget(), label='内容')
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='标签'
    )

    class Meta:
        model = Message
        fields = ['title', 'tags', 'content', 'image', 'status']
        labels = {
            'title': '标题',
            'status': '状态',
            'image': '图片',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 可以在此处添加其他初始化逻辑