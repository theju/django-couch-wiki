from django import forms
from wiki.models import Page

class PageForm(forms.Form):
    _id           = forms.CharField(widget = forms.HiddenInput, required=False)
    title         = forms.CharField(max_length = 100, 
                                    widget = forms.TextInput(attrs = {"size": 42}),
                                    required = True)
    contents      = forms.CharField(widget = forms.Textarea,
                                    required = False)
    login_to_edit = forms.BooleanField(required = False)

    def __init__(self, *args, **kwargs):
        if kwargs:
            self.db = kwargs.pop('db')
        super(PageForm, self).__init__(*args, **kwargs)


    def clean_title(self):
        input_title  = self.cleaned_data['title']
        title_exists = Page.get_pages(self.db, key=input_title).rows
        if title_exists and not self.cleaned_data['_id'] == title_exists[0].value['_id']:
            raise forms.ValidationError("Title %s already exists" %title_exists[0].value['title'])
        return input_title
