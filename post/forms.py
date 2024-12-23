from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    PREFER_CHOICES = [
        ('სისხლი', 'სისხლი'),
        ('მოხუცი', 'მოხუცი'),
        ('ბავშვი', 'ბავშვი'),
        ('შშმ პირი', 'შშმ პირი'),
        ('გარემო', 'გარემო'),
        ('საკვები', 'საკვები'),
    ]



    prefer = forms.MultipleChoiceField(
        choices=PREFER_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'სათაური', 'class': 'form-control'})
    )
    custom_input_1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'input-text',}))
    custom_input_2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'input-text'}))

    deadline_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'id': 'deadline-date',
        })
    )
    deadline_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
            'id': 'deadline-time',
        })
    )
    location = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'color:#660066;', 'placeholder': 'ქალაქი'})
    )
    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'აღწერა',
        'class': 'input-textarea',
        'id': 'description',
        'style': 'width: 100%; height: 100px;'
    }))

    picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'color:#660066;', 'accept': 'image/*'})
    )


    class Meta:
        model = Post
        fields = ['title', 'description', 'prefer', 'deadline_date', 'deadline_time', 'location',  'picture', 'custom_input_1', 'custom_input_2',]
