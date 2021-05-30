from django.test import TestCase

# Create your tests here.

from socialvoiceapp.models import City, Country, Profile, AudioMessage


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        Country.objects.create(name="United Kingdom")
        #Profile.objects.create(username='testing')

    def test_first_name_label(self):
        profile = Profile.objects.get(id=1)
        # field_label = profile._meta.get_field('username').verbose_name
        # self.assertEquals(field_label, 'username')

    # def test_last_name_label(self):
    #     author = Author.objects.get(id=1)
    #     field_label = author._meta.get_field('last_name').verbose_name
    #     self.assertEquals(field_label, 'last name')

    # def test_date_of_birth_label(self):
    #     author = Author.objects.get(id=1)
    #     field_label = author._meta.get_field('date_of_birth').verbose_name
    #     self.assertEquals(field_label, 'date of birth')

    # def test_first_name_max_length(self):
    #     author = Author.objects.get(id=1)
    #     max_length = author._meta.get_field('first_name').max_length
    #     self.assertEquals(max_length, 100)

    # def test_last_name_max_length(self):
    #     author = Author.objects.get(id=1)
    #     max_length = author._meta.get_field('last_name').max_length
    #     self.assertEquals(max_length, 100)