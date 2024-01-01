# coding: utf-8
"""
    ShaarPy :: Forms
"""
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, TextInput, Textarea, CheckboxInput, EmailInput, HiddenInput
from shaarpy.models import Links
from shaarpy.tools import url_cleaning


class LinksForm(ModelForm):
    """
        form to create / edit a note / link
    """

    class Meta:

        model = Links
        fields = ('url', 'title', 'image', 'text', 'tags', 'private', 'sticky')
        widgets = {
            'tags': TextInput(attrs={'class': 'form-control', 'placeholder': _('tags,tag2')}),
            'url': TextInput(attrs={'class': 'form-control',
                                    'placeholder': _('Drop an URL or leave if empty for creating a note')}),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': _('Note:')}),
            'image': TextInput(attrs={'class': 'form-control', 'placeholder': _('Image URL:')}),
            'text': Textarea(attrs={'class': 'form-control', 'placeholder': _('content')}),
            'private': CheckboxInput(attrs={'class': 'form-check-input'}),
            'sticky': CheckboxInput(attrs={'class': 'form-check-input'}),
            'url_hashed': HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get("url")
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if url is None and title is None and text == '':
            msg = _("You need to enter something in one of those fields 'URL' or 'Title' or 'Text'")
            self.add_error('url', msg)
            self.add_error('title', msg)
            self.add_error('text', msg)

    def clean_url(self):
        """
            remove unwanted query parameters
        """
        data = self.cleaned_data['url']
        return url_cleaning(data)

    def clean_tags(self):
        """
            remove extra space
        """
        unwanted_chars = '?./:;!#&@{}[]|$`\\^~*+=-_'
        data = self.cleaned_data['tags']
        if data:
            if any(s in unwanted_chars for s in data):
                msg = _(f"characters {unwanted_chars} not allowed.")
                self.add_error('tags', msg)

            if data.endswith(','):
                data = data[:-1]
            return data.replace(' ', '')


class MeForm(ModelForm):

    """
        form to edit the user's profile
    """

    class Meta:

        model = User
        fields = ('email', 'last_name')
        widgets = {
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Last name')}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email')}),
        }
