from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_user import current_user, login_required, roles_required
from app import db
from app.main.forms import EditProfileForm, ReviewForm, TastingForm, ScoreForm
from app.models import User, Review, Brand, Tasting,Club, Score
from app.main import bp
from werkzeug import secure_filename
import pathlib
import decimal
import flask.json
from app.utils import rotateImage
from sqlalchemy import func
from decimal import Decimal

class MaltgeezersJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MaltgeezersJSONEncoder, self).default(obj)

@bp.route('/add/dummy/<int:tasting_id>', methods=['GET', 'POST'])
@roles_required('reviewer')    # Use of @roles_required decorator
def add_placeholder(tasting_id):
    tasting = Tasting.query.filter_by(id=tasting_id).first()
    num_reviews = tasting.reviews.count()
    #get next number in order
    review = Review()
    review.order = num_reviews + 1
    review.name = "Mystery"
    #review.img_name = "mystery_bottle.jpg"
    review.tasting_id = tasting_id
    db.session.add(review)
    db.session.commit()
    flash('Your placeholder has been added')
    return redirect(url_for('main.tasting',tasting_id=tasting_id))

@bp.route('/add/<int:tasting_id>', methods=['GET', 'POST'])
@roles_required('reviewer')    # Use of @roles_required decorator
def add(tasting_id):
    form = ReviewForm(tasting_id = tasting_id)
    current_time = datetime.utcnow()
    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        # set age to 0 if it has not been entered
        if form.age.data == "":
            age = 0
        else:
            age = int(form.age.data)
        if form.brand_id.data is '0':
            brand = Brand(name=form.brand_name.data)
            db.session.add(brand)
            db.session.flush()
            review = Review(order=form.order.data,notes=form.notes.data, tasting_note=form.tasting_note.data,img_name=filename,  name=form.name.data, age = age, max_rating=form.max_rating.data, avg_rating = form.avg_rating.data, min_rating=form.min_rating.data, author=current_user, brand_id=brand.id, tasting_id = form.tasting_id.data)
        else:
            review = Review(order=form.order.data,notes=form.notes.data, tasting_note=form.tasting_note.data,img_name=filename, name=form.name.data, age = form.age.data, max_rating=form.max_rating.data, avg_rating = form.avg_rating.data, min_rating=form.min_rating.data, author=current_user, brand_id=form.brand_id.data, tasting_id = form.tasting_id.data)
        db.session.add(review)
        db.session.commit()

        pathlib.Path(current_app.config['UPLOAD_FOLDER'] + '/' + str(review.id)).mkdir(parents=True, exist_ok=True)
        form.image.data.save(current_app.config['UPLOAD_FOLDER']  + '/' + str(review.id) + '/' + filename)
        rotateImage(current_app.config['UPLOAD_FOLDER']  + '/' + str(review.id) + '/',filename)
        flash('Your review is now live!')
        return redirect(url_for('main.tasting',tasting_id=form.tasting_id.data))
    return render_template('add_review.html', title='Add Review', form=form,)

@bp.route("/review/edit/<int:review_id>", methods=['GET', 'POST'])
def edit_review(review_id):
    review = Review.query.filter_by(id=review_id).first()
    form = ReviewForm(obj=review)
    if review.brand is not None:
        form.brand_name.data = review.brand.name
    if form.validate_on_submit:
        if request.method == 'POST':
            if form.age.data == "":
                age = 0
            else:
                age = int(form.age.data)
            if form.brand_id.data is '0':
                brand = Brand(name=form.brand_name.data)
                db.session.add(brand)
                db.session.flush()
                review.brand_id=brand.id
            else:
                review.brand_id=form.brand_id.data
            review.order = form.order.data
            review.notes=form.notes.data
            review.tasting_note=form.tasting_note.data
            review.name=form.name.data
            review.age=age
            review.max_rating=form.max_rating.data
            review.avg_rating = form.avg_rating.data
            review.min_rating=form.min_rating.data
            review.author=current_user
            if form.image.data is not None:
                filename = secure_filename(form.image.data.filename)
                pathlib.Path(current_app.config['UPLOAD_FOLDER'] + '/' + str(review.id)).mkdir(parents=True, exist_ok=True)
                form.image.data.save(current_app.config['UPLOAD_FOLDER']  + '/' + str(review.id) + '/' + filename)
                review.img_name = filename
                rotateImage(current_app.config['UPLOAD_FOLDER']  + '/' + str(review.id) + '/',filename)

            db.session.commit()
            flash('Your changes have been saved.' )
            return redirect(url_for('main.tasting',tasting_id=review.tasting.id))
    return render_template('add_review.html', title='Edit Review', action="Edit", form=form)

@bp.route('/add_tasting', methods=['GET', 'POST'])
@roles_required('reviewer')
def add_tasting():
    form = TastingForm()
    form.club_id.choices=[(row.id, row.name) for row in Club.query.all()]
    if form.validate_on_submit():
        if form.num_attendees.data == "":
            attendees = None
        else:
            attendees = int(form.num_attendees.data)
        tasting = Tasting(date=form.date.data, location=form.location.data, num_attendees=attendees, club_id=form.club_id.data)
        db.session.add(tasting)
        db.session.commit()
        flash('Your tasting is now live, add some whiskies!')
        return redirect(url_for('main.tastings'))
    return render_template('add_tasting.html', title='Add Tasting', form=form,)

@bp.route('/tastings', methods=['GET'])
def tastings():
    tastings = Tasting.query.order_by(Tasting.date.desc())
    return render_template("tastings.html", title='Tastings', tastings=tastings)

@bp.route('/tasting/<int:tasting_id>', methods=['GET'])
def tasting(tasting_id):
    tasting = Tasting.query.filter_by(id=tasting_id).first()
    return render_template("tasting.html", title='Tasting', tasting=tasting, description="Our tasting notes from the " + tasting.date.strftime('%d/%m/%Y') + " meetup.")

@bp.route('/review/<int:review_id>', methods=['GET','POST'])
def review(review_id):
    review = Review.query.filter_by(id=review_id).first()
    form=ScoreForm()
    form.review_id.data = review.id
    if form.validate_on_submit:
        if request.method == 'POST':
            scores = form.score.data.split(",")
            for s in scores:
                score = Score(review_id=review.id, score=Decimal(s), notes=form.notes.data)
                db.session.add(score)
            # Update the average score
            review.avg_rating = review.avg()
            db.session.commit()
            flash('Your score has been added.')
            return redirect(url_for('main.review', review_id=review.id))
    return render_template("bottle.html", title='Review of ' + review.title(), form=form,review=review, description=review.notes, image_url=review.img_url_external() )

@bp.route("/tasting/edit/<int:tasting_id>", methods=['GET', 'POST'])
def edit_tasting(tasting_id):
    tasting = Tasting.query.filter_by(id=tasting_id).first()
    form = TastingForm(obj=tasting)
    form.club_id.choices=[(row.id, row.name) for row in Club.query.all()]
    if form.validate_on_submit:
        if request.method == 'POST':
            tasting.date = form.date.data
            tasting.location = form.location.data
            tasting.num_attendees = form.num_attendees.data
            tasting.club_id = form.club_id.data
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('main.tastings'))
    return render_template('add_tasting.html', title='Edit Tasting', action="Edit", form=form)

@bp.route('/attend/<int:tasting_id>')
@login_required
def attend(tasting_id):
    tasting = Tasting.query.filter_by(id=tasting_id).first()
    if tasting is None:
        flash('Tasting {} not found.'.format(tasting_id))
        return redirect(url_for('main.index'))
    current_user.attend(tasting)
    db.session.commit()
    flash('You are attending {}!'.format(tasting.date))
    if "sign-in" not in request.referrer:
        return redirect(request.referrer)
    else:
        return redirect(url_for('main.tastings'))
    #return redirect(url_for('main.tasting', tasting_id=tasting_id))

@bp.route('/unattend/<int:tasting_id>')
@login_required
def unattend(tasting_id):
    tasting = Tasting.query.filter_by(id=tasting_id).first()
    if tasting is None:
        flash('Tasting {} not found.'.format(tasting_id))
        return redirect(url_for('main.index'))
    current_user.unattend(tasting)
    db.session.commit()
    flash('You are not attending {}!'.format(tasting.date))
    return redirect(request.referrer)
    # return redirect(url_for('main.tasting', tasting_id=tasting_id))

@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    current_time = datetime.utcnow()
    reviews = Review.query.filter(Review.avg_rating != None).order_by(Review.avg_rating.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    latest_tasting = Tasting.query.filter(Tasting.date < current_time, Tasting.reviews != None).order_by(Tasting.date.desc()).limit(1)
    return render_template("index.html", title='Home', reviews=reviews.items, tasting=latest_tasting[0])

@bp.route('/reviews')
def reviews():
    page = request.args.get('page', 1, type=int)
    reviews = Review.query.order_by(Review.avg_rating.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    return render_template("reviews.html", title='All Reviews', reviews=reviews)


@bp.route('/about')
def about():
    return render_template("about.html", title='About')

@bp.route('/cookiepolicy')
def cookiepolicy():
    return render_template("cookiepolicy.html", title='Cookie Policy')

@bp.route('/contact')
def contact():
    return render_template("contact.html", title='Contact')

@bp.route('/charts')
def charts():
    return render_template("charts.html", title='Charts')

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
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.user',username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data  = current_user.about_me
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
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
