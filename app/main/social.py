import urllib.request
from app.main import bp
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_user import current_user, login_required, roles_required
import json
import facebook
from twython import Twython
from config import Config
from app.models import Tasting

# Facebook not yet working du eto app permissions.
def fetch_app_access_token(fb_app_id, fb_app_secret):
    url = 'https://graph.facebook.com/oauth/access_token?client_id=' + fb_app_id + '&client_secret=' + fb_app_secret +'&grant_type=client_credentials'
    with urllib.request.urlopen(url) as resp:
        b=resp.read()
    if resp.getcode() == 200:
        current_app.logger.info(type(b))
        # Decode UTF-8 bytes to Unicode, and convert single quotes
        # to double quotes to make it valid JSON
        my_json = b.decode('utf8').replace("'", '"')

        # Load the JSON to a Python list & dump it back out as formatted JSON
        data = json.loads(my_json)
        return data['access_token']
    else:
        return None



@bp.route('/post/facebook/', methods=['GET', 'POST'])
@roles_required('reviewer')
def fb_post():
  graph = facebook.GraphAPI(access_token=fetch_app_access_token(config['FB_APP_ID'], config['FB_APP_SECRET']))
  graph.put_object("411526795925491", "feed", message="posted from the site")
  flash("posted")
  return redirect(url_for('main.tastings'))

@bp.route('/twitter/tasting/<int:tasting_id>', methods=['GET', 'POST'])
@roles_required('reviewer')
def tweet_tasting(tasting_id):
    twitter = Twython(
        current_app.config['TWITTER_CONSUMER_KEY'],
        current_app.config['TWITTER_CONSUMER_SECRET'],
        current_app.config['TWITTER_ACCESS_TOKEN'],
        current_app.config['TWITTER_ACCESS_TOKEN_SECRET']
    )
    tasting = Tasting.query.filter_by(id=tasting_id).first()
    distilleries = ""
    for review in tasting.reviews:
        if review.brand is not None:
            distilleries = distilleries + "#" + review.brand.name.replace(" ","") + " "

    message = "Checkout our latest tasting " + distilleries + " " + url_for('main.tasting', tasting_id=tasting_id,  _external=True)
    twitter.update_status(status=message)
    flash("Tweeted: {}".format(message))
    return redirect(url_for('main.tasting', tasting_id=tasting_id))

@bp.route('/twitter/review/<int:review_id>', methods=['GET', 'POST'])
@roles_required('reviewer')
def tweet_review(review_id):
    twitter = Twython(
        current_app.config['TWITTER_CONSUMER_KEY'],
        current_app.config['TWITTER_CONSUMER_SECRET'],
        current_app.config['TWITTER_ACCESS_TOKEN'],
        current_app.config['TWITTER_ACCESS_TOKEN_SECRET']
    )
    review = Review.query.filter_by(id=review_id).first()

    message = "Checkout our " + str(review.avg_rating) + "/10 review of " + review.title + " " + url_for('main.review', review_id=review_id,  _external=True)
    twitter.update_status(status=message)
    flash("Tweeted: {}".format(message))
    return redirect(url_for('main.review',review_id=review_id))
