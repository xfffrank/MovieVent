from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
    # content = forms.CharField(max_length=280, label='')

    # 测试 max_length 和 Textarea 是否冲突
    # content = forms.CharField(max_length=280, label='', widget=forms.Textarea)
