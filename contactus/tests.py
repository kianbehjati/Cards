from django.test import TestCase
from django.urls import reverse
from .models import Contact

class ContactUsTests(TestCase):

    def test_contact_page_get(self):
        # GET request to contact page
        url = reverse("contactus")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIsNone(response.context["status"])

    def test_contact_page_post_success(self):
        # POST with valid data
        url = reverse("contactus")
        data = {
            "title": "Feedback",
            "text": "This is some test feedback text.",
            "email": "user@example.com"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact.html")
        self.assertEqual(response.context["form_status"], "sent")
        
        # Verify Contact object was created in database
        self.assertEqual(Contact.objects.count(), 1)
        contact_obj = Contact.objects.first()
        self.assertEqual(contact_obj.title, "Feedback")
        self.assertEqual(contact_obj.text, "This is some test feedback text.")
        self.assertEqual(contact_obj.email, "user@example.com")

    def test_contact_page_post_invalid(self):
        # POST with invalid data
        url = reverse("contactus")
        data = {
            "title": "",
            "text": "Too short/no title",
            "email": "not-an-email"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        
        # form not valid
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        self.assertIn("email", form.errors)
      
        self.assertEqual(Contact.objects.count(), 0)
