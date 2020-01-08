from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Profile


User = get_user_model()

class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cfe', password='somepassword')
        self.userb = User.objects.create_user(username='cfe-2', password='somepassword2')
    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')
        return client

    def test_profile_created_via_signal(self):
        qs = Profile.objects.all()
        self.assertEqual(qs.count(), 2)
    
    def test_following(self):
        first = self.user
        second = self.userb
        first.profile.followers.add(second) # added a follower
        second_user_following_whom = second.following.all()
        qs = second_user_following_whom.filter(user=first) # from a user, check other user is being followed.
        first_user_following_no_one = first.following.all() # check new user has is not following anyone
        self.assertTrue(qs.exists())
        self.assertFalse(first_user_following_no_one.exists())

    def test_follow_api_endpoint(self):
        client = self.get_client()
        response = client.post(
            f"/api/profiles/{self.userb.username}/follow",
            {"action": "follow"}
        )
        r_data = response.json()
        count = r_data.get("count")
        self.assertEqual(count, 1)
    
    def test_unfollow_api_endpoint(self):
        first = self.user
        second = self.userb
        first.profile.followers.add(second)
        client = self.get_client()
        response = client.post(
            f"/api/profiles/{self.userb.username}/follow",
            {"action": "unfollow"}
        )
        r_data = response.json()
        count = r_data.get("count")
        self.assertEqual(count, 0)
    
    def test_cannot_follow_api_endpoint(self):
        client = self.get_client()
        response = client.post(
            f"/api/profiles/{self.user.username}/follow",
            {"action": "follow"}
        )
        r_data = response.json()
        count = r_data.get("count")
        self.assertEqual(count, 0)