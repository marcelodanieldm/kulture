from django import forms
from .models import Post, BlogCategory

class PostForm(forms.ModelForm):
    scheduled_for = forms.DateTimeField(required=False, widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    tags = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Tag
        self.fields['tags'].queryset = Tag.objects.all()

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'scheduled_for', 'published', 'tags', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
