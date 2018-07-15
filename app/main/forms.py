from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField,DecimalField, HiddenField, DateTimeField, SelectField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import User
from flask_user import UserManager

# Customize the Register form:
from flask_user.forms import RegisterForm
class MaltgeezersRegisterForm(RegisterForm):
    # Add a name fields to the Register form
    first_name = StringField(('First Name'), validators=[DataRequired()])
    last_name = StringField(('Last Name'), validators=[])

# Customize Flask-Userto support registration form
class MaltgeezersUserManager(UserManager):
    def customize(self, app):
        # Configure customized forms
        self.RegisterFormClass = MaltgeezersRegisterForm

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name')
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class ReviewForm(FlaskForm):
    brand_id = HiddenField('Brand',id="brand_id")
    brand_name = HiddenField('Brand Name',id="brand_name")
    tasting_id = HiddenField('Tasting Date',id="tasting_id")
    order = IntegerField('Bottle Number (1,2,3,...)', validators=[DataRequired()])
    name = StringField('Bottle Name', validators=[DataRequired()])
    age = StringField('Age')
    notes = TextAreaField('Notes', validators=[
        DataRequired(), Length(min=1, max=2000)], id="notes")
    tasting_note = TextAreaField('Tasting', validators=[
            DataRequired(), Length(min=1, max=2000)],id="tasting")
    max_rating = DecimalField('Max Score', validators=[DataRequired(),NumberRange(0, 10)])
    avg_rating = DecimalField('Average Score', validators=[DataRequired(),NumberRange(0, 10)])
    min_rating = DecimalField('Min Score', validators=[DataRequired(),NumberRange(0,10)])
    image = FileField("Bottle Image (450 x 600 px)", validators=[
        FileAllowed(['jpg', 'png'], 'jpg and png Images only!')])
    submit = SubmitField('Submit')

class TastingForm(FlaskForm):
    date = DateTimeField('Tasting Date (dd-mm-YYYY HH:MM)', validators=[DataRequired()],format='%d-%m-%Y %H:%M')
    club_id = SelectField('Club',coerce=int, validators=[DataRequired()])
    location = StringField('Location')
    num_attendees = StringField('Number of Attendees')
    submit = SubmitField('Submit')

class ScoreForm(FlaskForm):
    review_id = HiddenField('Review',id="review_id")
    score = DecimalField('Score', validators=[DataRequired(),NumberRange(0,10)])
    notes = StringField('Note')
    submit = SubmitField('Add')
