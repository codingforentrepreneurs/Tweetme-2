from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from .models import Profile


User = get_user_model()

class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cfe', password='somepassword')
        self.userb = User.objects.create_user(username='cfe-2', password='somepassword2')
    
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

