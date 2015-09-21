from __future__ import absolute_import

from flask import Flask, request, Blueprint, current_app
import os
import re
from travispy import TravisPy
import logging


LOG_LEVEL = logging.INFO
OUTPUT_FOLDER = '/tmp/pylint-server'
VALID_REPOS = []
BADGE_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="85" height="20">
  <linearGradient id="a" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <!-- whole rectangle -->
  <rect rx="3" width="85" height="20" fill="#555"/>

  <!-- rating part -->
  <rect rx="3" x="50" width="35" height="20" fill="#{1}"/>
  <path fill="#{1}" d="M50 0h4v20h-4z"/>

  <!-- whole rectangle -->
  <rect rx="3" width="85" height="20" fill="url(#a)"/>

  <g fill="#fff" text-anchor="middle"
                 font-family="DejaVu Sans,Verdana,Geneva,sans-serif"
                 font-size="11">
    <text x="25" y="15" fill="#010101" fill-opacity=".3">pylint</text>
    <text x="25" y="14">pylint</text>
    <text x="67" y="15" fill="#010101" fill-opacity=".3">{0:.2f}</text>
    <text x="67" y="14">{0:.2f}</text>
  </g>
</svg>
"""

mainbp = Blueprint('main', __name__)


@mainbp.route('/reports', methods=['POST'])
def handle_report_post():
    current_app.logger.info('handling POST on /reports')
    travis_job_id_str = None
    if 'travis-job-id' in request.form:
        travis_job_id_str = request.form['travis-job-id']

    report = None
    if 'pylint-report' in request.files:
        report = request.files['pylint-report'].read()

    slug = get_repo_slug(int(travis_job_id_str))
    valid_repos = current_app.config['VALID_REPOS']
    if slug and (not valid_repos or slug in valid_repos):
        output_folder = current_app.config['OUTPUT_FOLDER']
        output_report = os.path.join(output_folder, slug, 'report.html')
        current_app.logger.info('saving report to '+output_report)
        save_file(output_report, report)

        (rating, colour) = get_rating_and_colour(report)
        output_badge = os.path.join(output_folder, slug, 'rating.svg')
        current_app.logger.info('saving badge to '+output_badge)
        save_file(output_badge, BADGE_TEMPLATE.format(rating, colour))
        return 'OK\n', 200
    else:
        raise ValueError('invalid repository slug')


def get_rating_and_colour(report):
    colour = '9d9d9d'
    rating = 0
    match = re.search("Your code has been rated at (.+?)/10", report)
    if match:
        rating = float(match.group(1))
        if rating >= 9 and rating <= 10:
            colour = '44cc11'
        elif rating < 9 and rating >= 7:
            colour = 'f89406'
        elif rating >= 0 and rating < 7:
            colour = 'b94947'
        else:
            colour = '9d9d9d'
    return (rating, colour)


def get_repo_slug(travis_job_id):
    current_app.logger.info('getting repo slug, contacting travis...')
    travis = TravisPy.github_auth(os.environ["GITHUB_TOKEN"])
    job = travis.job(travis_job_id)
    repo = travis.repo(job.repository_id)
    current_app.logger.info('returning slug: '+repo.slug)
    return repo.slug


def save_file(filename, contents):
    """Save a file anywhere"""
    ensure_path(os.path.dirname(filename))
    with open(filename, 'w') as thefile:
        thefile.write(unicode(contents))


def ensure_path(path):
    """Make sure the path exists, creating it if need be"""
    if not os.path.exists(path):
        os.makedirs(path)


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.logger.setLevel(app.config['LOG_LEVEL'])
    app.register_blueprint(mainbp)
    return app
