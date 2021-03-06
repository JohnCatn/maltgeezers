from datetime import datetime, timedelta
from hashlib import md5
from time import time
from flask import current_app, url_for
from flask_user import UserManager, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
# from app import db, login
from app import db
import base64
import os
from app.utils import mean

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data
    @staticmethod
    def to_collection_dict_all(query, **kwargs):
        resources = query.all()
        data = {
            'items': [item.to_dict() for item in resources],
        }
        return data

    @staticmethod
    def to_chart_dict_all(query, **kwargs):
        resources = query.all()
        data = {
            'items': [item.to_chart_data() for item in resources],
        }
        return data


class Tasting(db.Model):
    __tablename__ = 'tasting'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(300), nullable=True)
    num_attendees = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    reviews = db.relationship('Review', backref='tasting', lazy='dynamic')

    def __repr__(self):
        return '<Tasting {}>'.format(self.id)

    def to_dict(self):

        data = {
            'id': self.id,
            'date': self.date,
            'location': self.location,
            '_links': {
                'self': url_for('api.get_review', id=self.id),
                'review': url_for('main.review', review_id=self.id,_external=True)
            }
        }
        if self.reviews is not None:
            data['review'] = {
                'items': [item.to_chart_data() for item in self.reviews]
            }
        return data

# Define the Role data-model
class Club(db.Model):
    __tablename__ = 'club'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    postcode = db.Column(db.String(10), unique=True)
    tastings = db.relationship('Tasting', backref='club', lazy='dynamic')

class UserClubs(db.Model):
    __tablename__ = 'user_club'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    club_id = db.Column(db.Integer(), db.ForeignKey('club.id', ondelete='CASCADE'))

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

class UserTasting(db.Model):
    __tablename__= 'user_tasting'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    tasting_id = db.Column(db.Integer(), db.ForeignKey('tasting.id', ondelete='CASCADE'))


class User(db.Model, UserMixin, PaginatedAPIMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information (required for Flask-User)
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User fields
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=True)
    about_me = db.Column(db.String(140), nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    reviews = db.relationship('Review', backref='author', lazy='dynamic')
    hosted = db.relationship('Tasting', backref='host', lazy='dynamic')
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_role',
                            backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
    clubs = db.relationship('Club', secondary='user_club',
                            backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
    tastings = db.relationship('Tasting', secondary='user_tasting',
                            backref=db.backref('attendees', lazy='dynamic'), lazy='dynamic')

    def has_role(self, *specified_role_names):
        """ Return True if the user has one of the specified roles. Return False otherwise.
            has_roles() accepts a 1 or more role name parameters
                has_role(role_name1, role_name2, role_name3).
            For example:
                has_roles('a', 'b')
            Translates to:
                User has role 'a' OR role 'b'
        """

        # Allow developers to attach the Roles to the User or the UserProfile object
        if hasattr(self, 'roles'):
            roles = self.roles
        else:
            if hasattr(self, 'user_profile') and hasattr(self.user_profile, 'roles'):
                roles = self.user_profile.roles
            else:
                roles = None
        if not roles: return False

        # Translates a list of role objects to a list of role_names
        user_role_names = [role.name for role in roles]

        # Return True if one of the role_names matches
        for role_name in specified_role_names:
            if role_name in user_role_names:
                return True

        # Return False if none of the role_names matches
        return False

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'last_seen': self.last_seen.isoformat() + 'Z',
            'review_count': self.reviews.count(),
            'follower_count': self.followers.count(),
            'followed_count': self.followed.count(),
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'followers': url_for('api.get_followers', id=self.id),
                'followed': url_for('api.get_followed', id=self.id),
                'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def attend(self, tasting):
        if not self.is_attending(tasting):
            self.tastings.append(tasting)

    def unattend(self, tasting):
        if self.is_attending(tasting):
            self.tastings.remove(tasting)

    def is_attending(self, tasting):
        user_tastings = [tasting.id for tasting in self.tastings]
        if tasting.id in user_tastings:
            return True
        return False

    def followed_reviews(self):
        followed = Review.query.join(
            followers, (followers.c.followed_id == Review.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Review.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Review.timestamp.desc())

# @login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Country(db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    regions = db.relationship('Region', backref='country', lazy='dynamic')

    def __repr__(self):
        return '<Country {}>'.format(self.name)

class Type(db.Model):
    __tablename__ = 'type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    brands  = db.relationship('Brand', backref='type', lazy='dynamic')

    def __repr__(self):
        return '<Type {}>'.format(self.name)

class Region(db.Model):
    __tablename__ = 'region'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    brands  = db.relationship('Brand', backref='region', lazy='dynamic')

    def __repr__(self):
        return '<Region {}>'.format(self.name)

class Brand(PaginatedAPIMixin, db.Model):
    __tablename__ = 'brand'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    type_id = db.Column(db.Integer,db.ForeignKey('type.id'))
    region_id = db.Column(db.Integer,db.ForeignKey('region.id'))
    reviews = db.relationship('Review', backref='brand', lazy='dynamic')

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'region': 'Unknown' if self.region is None else self.region.name
        }
        return data

    def __repr__(self):
        return '<Brand {}>'.format(self.name)

class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'))
    score = db.Column(db.Numeric(10,1))
    notes = db.Column(db.String(500))

class Review(PaginatedAPIMixin, db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(300), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.String(2000))
    tasting_note = db.Column(db.String(2000))
    max_rating = db.Column(db.Numeric(10,1))
    avg_rating = db.Column(db.Numeric(10,1))
    min_rating = db.Column(db.Numeric(10,1))
    img_name = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    brand_id = db.Column(db.Integer,db.ForeignKey('brand.id'))
    tasting_id = db.Column(db.Integer,db.ForeignKey('tasting.id'))
    scores = db.relationship('Score', backref='review', lazy='dynamic')

    def avg(self):
        if self.scores is not None:
            s = [item.score for item in self.scores]
            if len(s):
                return mean(s)
        return self.avg_rating

    def min(self):
        if self.scores is not None:
            s = [item.score for item in self.scores]
            if len(s):
                return min(s)
        return self.min_rating

    def max(self):
        if self.scores is not None:
                s = [item.score for item in self.scores]
                if len(s):
                    return max(s)
        return self.max_rating

    def title(self):
        title = ""
        if self.brand is not None:
            title = title + self.brand.name + " "
        if self.age != 0:
            title = title + str(self.age) + "yr old "
        title = title + self.name
        return title

    def img_url(self):
        filename = 'img/mystery_bottle.jpg' if self.img_name is None else'uploads/' + str(self.id) + '/' + self.img_name
        return url_for('static',filename=filename)

    def img_url_external(self):
        filename = 'img/mystery_bottle.jpg' if self.img_name is None else'uploads/' + str(self.id) + '/' + self.img_name
        return url_for('static',filename=filename, _external=True)

    def to_dict(self):

        data = {
            'id': self.id,
            'title': self.title(),
            'name': self.name,
            'age': self.age,
            'notes': self.notes,
            'tasting_notes': self.tasting_note,
            'max_rating': str(self.max()),
            'avg_rating': str(self.avg()),
            'min_rating': str(self.min()),
            'img_url': self.img_url(),
            '_links': {
                'self': url_for('api.get_review', id=self.id),
                'review': url_for('main.review', review_id=self.id,_external=True)
            }
        }
        if self.tasting is not None:
            data['tasting'] = {
                'date': '' if self.tasting.date is None else self.tasting.date.strftime('%d, %b %Y'),
                'location': 'somewhere' if self.tasting.location is None else self.tasting.location
            }
        if self.brand is not None:
            data['distillery'] = 'Unknown' if self.brand.name is None else self.brand.name
        return data

    def to_chart_data(self):

        data = {
            'name': self.name,
            'type':'box',
             'marker': {
                'color': 'rgb(8,81,156)'
              },
        }
        if self.scores is not None:
            #data['y'] = list(self.scores.values())
            data['y'] = [item.score for item in self.scores]
        return data

    def __repr__(self):
        return '<Review {}>'.format(self.name)
