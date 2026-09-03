from django.test import TestCase
from rest_framework.test import APIClient
from home.models import LinkedInProfile


class LinkedInSearchTests(TestCase) :

    def test_search_by_keyword(self) :
        profile = LinkedInProfile.objects.create(
            full_name = "عباس اسماعیلی",
            job_title = "توسعه‌دهنده",
            location = "همدان",
            skills = ["Python", "Django"]
        )

        client = APIClient()
        response = client.get('/api/search/', {'keyword' : 'عباس'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['full_name'], 'عباس اسماعیلی')

    def test_search_by_skill(self) :
        profile = LinkedInProfile.objects.create(
            full_name = "فرهاد اصغری",
            skills = ["React", "JavaScript"]
        )

        client = APIClient()
        response = client.get('/api/search/', {'skill' : 'React'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['full_name'], 'فرهاد اصغری')

    def test_search_no_results(self) :
        client = APIClient()
        response = client.get('/api/search/', {'keyword' : 'چیزی که نیست'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)