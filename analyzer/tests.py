from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from .models import Document


class DocumentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sample_file = SimpleUploadedFile(
            "test.txt",
            b"This is a test file content for testing purposes"
        )

    def test_document_upload(self):
        response = self.client.post(
            '/api/documents/',
            {'file': self.sample_file, 'title': 'Test Document'},
            format='multipart'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Document.objects.count(), 1)

    def test_tfidf_calculation(self):
        doc = Document.objects.create(
            title="Test",
            file=self.sample_file,
            content="test content"
        )
        response = self.client.get(f'/api/documents/{doc.id}/tfidf/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('test', response.data)
