""" Some trivial test to demo strate functionality """ 
import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import URLNotes


User = get_user_model()

class URLNotesModelTest(TestCase):
    """ Testing the models """
    def setUp(self):
        """Set up a test user for the tests."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_create_urlnotes(self):
        """Test that a URLNotes object is created correctly."""
        urlnote = URLNotes.objects.create(
            user=self.user,
            notes="Test note for URL",
            url="http://example.com"
        )

        # Check that the URLNotes object has been saved correctly
        self.assertEqual(urlnote.user, self.user)
        self.assertEqual(urlnote.notes, "Test note for URL")
        self.assertEqual(urlnote.url, "http://example.com")

    def test_uuid_generation(self):
        """Test that UUID is automatically generated when creating a URLNotes object."""
        urlnote = URLNotes.objects.create(
            user=self.user,
            notes="Another test note",
            url="http://example2.com"
        )

        # Ensure that the UUID is generated and is a valid UUID
        self.assertIsInstance(urlnote.uuid, uuid.UUID)
        self.assertTrue(urlnote.uuid)  # Ensure UUID is not empty

    def test_str_method(self):
        """Test the __str__ method of the URLNotes model."""
        urlnote = URLNotes.objects.create(
            user=self.user,
            notes="Test note for __str__",
            url="http://example.com"
        )

        # Check that the string representation of the model returns the notes
        self.assertEqual(str(urlnote), "Test note for __str__")
