from django.forms import ModelForm, Textarea, NumberInput, TextInput, Select, HiddenInput

from .models import Author, Writing

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        widgets = {
            'name' : TextInput(attrs={'placeholder': 'имя автора ...'}),
            'lang' : Select(attrs={'placeholder': 'язык ...'}),
        }

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w3-input w3-round-xlarge w3-light-gray p-1 my-1 mx-0'


class WritingForm(ModelForm):
    class Meta:
        model = Writing
        fields = '__all__'
        widgets = {
            'title' : TextInput(attrs={'placeholder': 'Название ...'}),
            'genre' : Select(attrs={'placeholder': 'язык ...'}),
            'active' : HiddenInput(),
            'hidden' : HiddenInput(),
            'is_sample' : HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(WritingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w3-input w3-round-xlarge w3-light-gray p-1 my-1 mx-0'

