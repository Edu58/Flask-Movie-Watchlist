import unittest

from app.models import Review, User


class TestReviews(unittest.TestCase):
    def Setup(self):
        self.user_james = User(username='john', email='john@gmail.com', password='johndoe256')
        self.new_review = Review(movie_id=1234, movie_title='James Bond', movie_review='Fantastic Movie',
                                 image_path='https://image.tmdb.org/t/p/w500/jdjdjdjn', user=self.user_james)

    def tearDown(self) -> None:
        Review.query.delete()
        User.query.delete()

    def test_instance_variables(self):
        self.assertEquals(self.new_review.movie_id, 12345)
        self.assertEquals(self.new_review.movie_title, 'James Bond')
        self.assertEquals(self.new_review.movie_review, 'Fantastic Movie')
        self.assertEquals(self.new_review.user, self.user_james)

    def test_get_review_by_id(self):
        self.new_review.save_review()
        got_reviews = Review.get_reviews(12345)
        self.assertTrue(len(got_reviews) == 1)


if __name__ == '__main__':
    unittest.main()
