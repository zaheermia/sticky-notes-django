from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    """Form for creating and editing notes."""

    class Meta:
        model = Note
        fields = ['title', 'content']
