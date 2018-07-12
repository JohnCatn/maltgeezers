from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField,DecimalField, HiddenField, DateTimeField, SelectField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import User


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
    name = StringField('Bottle Name', validators=[DataRequired()])
    age = StringField('Age')
    notes = TextAreaField('Notes', validators=[
        DataRequired(), Length(min=1, max=2000)], id="notes")
    tasting_note = TextAreaField('Tasting', validators=[
            DataRequired(), Length(min=1, max=2000)],id="tasting")
    max_rating = DecimalField('Max Score', validators=[DataRequired(),NumberRange(0, 10)])
    avg_rating = DecimalField('Average Score', validators=[DataRequired(),NumberRange(0, 10)])
    min_rating = DecimalField('Min Score', validators=[DataRequired(),NumberRange(0,10)])
    image = FileField("Bottle Image", validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'jpg and png Images only!')])
    submit = SubmitField('Submit')

class TastingForm(FlaskForm):
    date = DateTimeField('Tasting Date', validators=[DataRequired()],format='%d-%m-%Y %H:%M')
    club_id = SelectField('Club',coerce=int, validators=[DataRequired()])
    location = StringField('Location')
    num_attendees = IntegerField('Number of Attendees')
    submit = SubmitField('Submit')
