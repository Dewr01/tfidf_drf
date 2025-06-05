from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class AnalysisResult(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    tf = models.FloatField()
    idf = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-idf']


class CorpusDocument(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document {self.id}"
