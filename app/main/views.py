import markdown2
from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user

from . import main
from .forms import ReviewForm, Updateprofile
from .. import db, photos
from ..models import Review, User
from ..request import get_movies, get_movie, search_movie


@main.route('/', methods=['GET'])
@login_required
def index():
    """
    View root page function that returns the index page and its data
    """
    popular_movies = get_movies('popular')
    upcoming_movie = get_movies('upcoming')
    now_showing_movie = get_movies('now_playing')
    title = 'Home - Welcome to The best Movie Review Website Online'
    searched_movie = request.args.get('movie_query')

    if searched_movie:
        return redirect(url_for('search', movie_name=search_movie))
    else:
        return render_template('index.html', title=title, popular=popular_movies, upcoming=upcoming_movie,
                               now_showing=now_showing_movie)


@main.route('/movies/<int:movie_id>', methods=['GET'])
@login_required
def movies(movie_id):
    """
    View movie page function that returns the movie details page and its data
    :param movie_id:
    :return: list of movies
    """
    return render_template('movie.html', id=movie_id)


@main.route('/movie/<int:movie_id>')
@login_required
def movie(movie_id):
    """
    View movie page function that returns the movie details page and its data
    """

    the_movie = get_movie(movie_id)
    title = f'{the_movie.title}'
    movie_reviews = Review.get_reviews(movie_id)
    return render_template('movie.html', title=title, movie=the_movie, reviews=movie_reviews)


@main.route('/search/<movie_name>')
@login_required
def search(movie_name):
    """
    View function to display the search results
    """
    movie_name_list = movie_name.split(" ")
    movie_name_format = "+".join(movie_name_list)
    searched_movies = search_movie(movie_name_format)
    title = f'search results for {movie_name}'
    return render_template('search.html', movies=searched_movies)


@main.route('/movie/review/new/<int:id>', methods=['GET', 'POST'])
@login_required
def new_review(id):
    form = ReviewForm()
    movie = get_movie(id)

    if form.validate_on_submit():
        title = form.title.data
        review = form.review.data
        new_review = Review(movie_id=movie.id, movie_title=title, image_path=movie.poster, movie_review=review,
                            user=current_user)
        new_review.save_review()
        return redirect(url_for('main.movie', movie_id=movie.id))

    title = f'{movie.title} review'
    return render_template('new_review.html', title=title, review_form=form, movie=movie)


@main.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        abort(404)

    return render_template('profile/profile.html', user=user)


@main.route('/profile/<username>/update', methods=['GET', 'POST'])
@login_required
def updateprofile(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        abort(404)

    form = Updateprofile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('main.profile', username=username))

    return render_template('profile/update.html', form=form)


@main.route('/user/<username>/update-profile-pic', methods=['POST'])
@login_required
def upload_profile_pic(username):
    user = User.query.filter_by(username=username).first()

    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()

    return redirect(url_for('main.profile', username=username))


@main.route('/review/<int:id>')
@login_required
def single_review(id):
    review = Review.query.get(id)
    if review is None:
        abort(404)

    format_review = markdown2.markdown(review.movie_review, extras=['code-friendly', 'fenced-code-blocks'])
    return render_template('review.html', review='review', format_review=format_review)