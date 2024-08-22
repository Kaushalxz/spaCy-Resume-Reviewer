from django.db import models
import fitz  # PyMuPDF-
from django.conf import settings
import os
class Resume(models.Model):
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    text_content = models.TextField()
    analysis_results = models.JSONField(null=True)

    def save(self, *args, **kwargs):
        self.extract_text()
        super().save(*args, **kwargs)

    def extract_text(self):
        correct_path = os.path.join(settings.MEDIA_ROOT, self.file.name)
        if not os.path.exists(correct_path):
            print(f"File not found: {correct_path}")
            return
        try:
            doc = fitz.open(correct_path)
            text = ""
            for page in doc:
                text += page.get_text()
            self.text_content = text
        except Exception as e:
            print(f"Error processing file {correct_path}: {e}")