from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, ReviewForm, TastingForm
from app.models import User, Review, Brand, Tasting
from app.main import bp
from werkzeug import secure_filename
import pathlib


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ReviewForm()
    current_time = datetime.utcnow()
    form.tasting_id.choices = [(row.id, row.date) for row in Tasting.query.filter(Tasting.date < current_time).all()]
    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        if form.brand_id.data is '0':
            brand = Brand(name=form.brand_name.data)
            db.session.add(brand)
            db.session.flush()
            review = Review(notes=form.review.data, tasting_note=form.tasting_note.data,img_name=filename,  name=form.name.data, age = form.age.data, max_rating=form.max_rating.data, avg_rating = form.avg_rating.data, min_rating=form.min_rating.data, author=current_user, brand_id=brand.id, tasting_id = form.tasting_id.data)
        else:
            review = Review(notes=form.notes.data, tasting_note=form.tasting_note.data,img_name=filename, name=form.name.data, age = form.age.data, max_rating=form.max_rating.data, avg_rating = form.avg_rating.data, min_rating=form.min_rating.data, author=current_user, brand_id=form.brand_id.data, tasting_id = form.tasting_id.data)
        db.session.add(review)
        db.session.commit()

        pathlib.Path(current_app.config['UPLOAD_FOLDER'] + '/' + str(review.id)).mkdir(parents=True, exist_ok=True)
        form.image.data.save(current_app.config['UPLOAD_FOLDER']  + '/' + str(review.id) + '/' + filename)
        flash('Your review is now live!')
        return redirect(url_for('main.index'))
    return render_template('add_review.html', title='Add Review', form=form,)

@bp.route('/add_tasting', methods=['GET', 'POST'])
@login_required
def add_tasting():
    form = TastingForm()
    if form.validate_on_submit():
        tasting = Tasting(date=form.date.data, location=form.location.data)
        db.session.add(tasting)
        db.session.commit()
        flash('Your tasting is now live!')
        return redirect(url_for('main.index'))
    return render_template('add_tasting.html', title='Add Tasting', form=form,)

@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    current_time = datetime.utcnow()
    reviews = Review.query.order_by(Review.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    latest_tasting = Tasting.query.filter(Tasting.date < current_time).order_by(Tasting.date.desc()).limit(1)
    next_url = url_for('main.index', page=reviews.next_num) \
        if reviews.has_next else None
    prev_url = url_for('main.index', page=reviews.prev_num) \
        if reviews.has_prev else None
    return render_template("index.html", title='Home', reviews=reviews.items, tasting=latest_tasting[0], next_url=next_url,
                           prev_url=prev_url)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    reviews = user.reviews.order_by(Review.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=reviews.next_num) \
        if reviews.has_next else None
    prev_url = url_for('main.user', username=user.username, page=reviews.prev_num) \
        if reviews.has_prev else None
    return render_template('user.html', user=user, reviews=reviews.items,
                           next_url=next_url, prev_url=prev_url)

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.user',username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('main.user', username=username))
