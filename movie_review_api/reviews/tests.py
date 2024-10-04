from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Review, Like, Comment


# Create test user, review, movie, and rating
class ReviewAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='cronaldo@gmail.com', password='testing', username='ororo'
        )
        self.client.force_authenticate(user=self.user)
        self.review = Review.objects.create(
            movie_title="Modern Family",
            content="One of the best comedy series of all time!",
            rating=4,
            user=self.user
        )

    def tearDown(self):
        # Cleanup after each test if necessary
        pass

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Review, Like

class LikeAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='messi@gmail.com', password='testpass', username='m10'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create a review to be liked
        self.review = Review.objects.create(
            movie_title="Test Movie",
            content="Great movie!",
            rating=4,
            user=self.user
        )

    def test_like_review(self):
        """
        Test that a user can like a review.
        """
        response = self.client.post('/api/likes/', {'review': self.review.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.first().review, self.review)
        self.assertEqual(Like.objects.first().user, self.user)

    def test_like_review_multiple_times(self):
        """
        Test that a user cannot like the same review more than once.
        """
        # Like the review for the first time
        self.client.post('/api/likes/', {'review': self.review.id})
        
        # Attempt to like the same review again
        response = self.client.post('/api/likes/', {'review': self.review.id})
        self.assertEqual(response.status_code, 400)
        self.assertIn('You have already liked this review.', response.data['detail'])

    def test_unlike_review(self):
        """
        Test that a user can unlike a review by deleting their like.
        """
        # Like the review first
        self.client.post('/api/likes/', {'review': self.review.id})
        like = Like.objects.first()
        
        # Unlike (delete) the like
        response = self.client.delete(f'/api/likes/{like.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Like.objects.count(), 0)

    def tearDown(self):
        # Cleanup after each test
        pass

# Testing the GET Request for a Review
def test_get_reviews(self):
    response = self.client.get('/reviews/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn("Test Movie", str(response.data))

# Testing the POST Request for Creating a Review
def test_create_review(self):
    data = {
        "movie_title": "Iron Man",
        "content": "A very exciting movie!",
        "rating": 5
    }
    response = self.client.post('/reviews/', data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Review.objects.count(), 2)

# Testing the PUT Request for Updating a Review
def test_update_review(self):
    data = {
        "movie_title": "Fantastic 4",
        "content": "Love it!",
        "rating": 4
    }
    response = self.client.put(f'/reviews/{self.review.id}/', data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.review.refresh_from_db()
    self.assertEqual(self.review.movie_title, "Fantastic 4")

# Testing the DELETE Request
def test_delete_review(self):
    response = self.client.delete(f'/reviews/{self.review.id}/')
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Review.objects.count(), 0)
