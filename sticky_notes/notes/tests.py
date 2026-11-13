"""Unit tests for the notes app: model, form and CRUD views."""
from django.test import TestCase
from django.urls import reverse

from .forms import NoteForm
from .models import Note


class NoteModelTest(TestCase):
    """Tests for the Note model."""

    def setUp(self):
        self.note = Note.objects.create(
            title='Test Note', content='This is a test note.'
        )

    def test_note_has_title(self):
        self.assertEqual(self.note.title, 'Test Note')

    def test_note_has_content(self):
        self.assertEqual(self.note.content, 'This is a test note.')

    def test_note_has_created_at(self):
        self.assertIsNotNone(self.note.created_at)

    def test_note_str_returns_title(self):
        self.assertEqual(str(self.note), 'Test Note')


class NoteFormTest(TestCase):
    """Tests for the NoteForm ModelForm."""

    def test_form_valid_with_title_and_content(self):
        form = NoteForm(data={'title': 'Milk', 'content': 'Buy milk'})
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_title(self):
        form = NoteForm(data={'title': '', 'content': 'No title here'})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


class NoteViewTest(TestCase):
    """Tests for the list, detail, create, update and delete views."""

    def setUp(self):
        self.note = Note.objects.create(
            title='Test Note', content='This is a test note.'
        )

    def test_note_list_view(self):
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')

    def test_note_detail_view(self):
        response = self.client.get(
            reverse('note_detail', args=[self.note.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
        self.assertContains(response, 'This is a test note.')

    def test_note_detail_view_missing_note_returns_404(self):
        response = self.client.get(reverse('note_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_note_create_view_get(self):
        response = self.client.get(reverse('note_create'))
        self.assertEqual(response.status_code, 200)

    def test_note_create_view_post(self):
        response = self.client.post(
            reverse('note_create'),
            {'title': 'New Note', 'content': 'Fresh content'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Note.objects.filter(title='New Note').exists())

    def test_note_create_view_post_invalid_creates_nothing(self):
        response = self.client.post(
            reverse('note_create'), {'title': '', 'content': 'No title'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 1)

    def test_note_update_view_post(self):
        response = self.client.post(
            reverse('note_update', args=[self.note.pk]),
            {'title': 'Updated', 'content': 'Updated content'},
        )
        self.assertEqual(response.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated')
        self.assertEqual(self.note.content, 'Updated content')

    def test_note_update_view_missing_note_returns_404(self):
        response = self.client.get(reverse('note_update', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_note_delete_view_post(self):
        response = self.client.post(
            reverse('note_delete', args=[self.note.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_note_delete_view_missing_note_returns_404(self):
        response = self.client.get(reverse('note_delete', args=[9999]))
        self.assertEqual(response.status_code, 404)
