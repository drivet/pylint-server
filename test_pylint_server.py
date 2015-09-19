from flask.ext.testing import TestCase
from pylint_server import create_app
import pylint_server
import shutil
import os

class FakeTravisApi(object):
    def __init__(self, job, repo):
        self.token = None
        self.job = job
        self.repo = repo

    def github_auth(self, token):
        self.token = token
        return FakeTravis(self.job, self.repo)


class FakeTravis(object):
    def __init__(self, job, repo):
        self._job = job
        self._repo = repo
        self.jobid = None
        self.repoid = None

    def job(self,jobid):
        self.jobid = jobid
        return self._job

    def repo(self,repoid):
        self.repoid = repoid
        return self._repo
        

class FakeJob(object):
    def __init__(self, jobid, repoid):
        self.jobid = jobid
        self.repository_id = repoid


class FakeRepo(object):
    def __init__(self, slug):
        self.slug = slug
    

POST_DATA = """
12345&Blah Blah Blah
Foo Foo Foo
Your code has been rated at {0}/10
La di da
"""

class PylintServerIntegrationTest(TestCase):

    def create_app(self):
        return create_app()
        
    def test_report_generated(self):
        old_environ = pylint_server.os.environ
        pylint_server.os.environ = {'GITHUB_TOKEN': 'AWESOMETOKEN'}

        old_travis_api = pylint_server.TravisPy
        pylint_server.TravisPy = FakeTravisApi(FakeJob(jobid=123, repoid=456),
                                               FakeRepo(slug='drivet/yawt'))

        response = self.client.post('/reports', data=POST_DATA.format('9.5'))
        self.assertTrue(os.path.exists('/tmp/pylint-server/drivet/yawt/report.html'))
        self.assertTrue(os.path.exists('/tmp/pylint-server/drivet/yawt/rating.svg'))
        self.assertTrue('9.5' in load_file('/tmp/pylint-server/drivet/yawt/rating.svg'))
      
        pylint_server.TravisPy = old_travis_api
        pylint_server.os.environ = old_environ

    def test_rating_greater_than_9_generates_green_badge(self):
        old_environ = pylint_server.os.environ
        pylint_server.os.environ = {'GITHUB_TOKEN': 'AWESOMETOKEN'}

        old_travis_api = pylint_server.TravisPy
        pylint_server.TravisPy = FakeTravisApi(FakeJob(jobid=123, repoid=456),
                                               FakeRepo(slug='drivet/yawt'))

        response = self.client.post('/reports', data=POST_DATA.format('9.5'))
        self.assertTrue('44cc11' in load_file('/tmp/pylint-server/drivet/yawt/rating.svg'))
      
        pylint_server.TravisPy = old_travis_api
        pylint_server.os.environ = old_environ
 
    def test_rating_greater_than_7_generates_orange_badge(self):
        old_environ = pylint_server.os.environ
        pylint_server.os.environ = {'GITHUB_TOKEN': 'AWESOMETOKEN'}

        old_travis_api = pylint_server.TravisPy
        pylint_server.TravisPy = FakeTravisApi(FakeJob(jobid=123, repoid=456),
                                               FakeRepo(slug='drivet/yawt'))

        response = self.client.post('/reports', data=POST_DATA.format('7.1'))
        self.assertTrue('f89406' in load_file('/tmp/pylint-server/drivet/yawt/rating.svg'))
      
        pylint_server.TravisPy = old_travis_api
        pylint_server.os.environ = old_environ

    def test_rating_less_than_7_generates_red_badge(self):
        old_environ = pylint_server.os.environ
        pylint_server.os.environ = {'GITHUB_TOKEN': 'AWESOMETOKEN'}

        old_travis_api = pylint_server.TravisPy
        pylint_server.TravisPy = FakeTravisApi(FakeJob(jobid=123, repoid=456),
                                               FakeRepo(slug='drivet/yawt'))

        response = self.client.post('/reports', data=POST_DATA.format('6'))
        self.assertTrue('b94947' in load_file('/tmp/pylint-server/drivet/yawt/rating.svg'))
      
        pylint_server.TravisPy = old_travis_api
        pylint_server.os.environ = old_environ

    def tearDown(self):
        if os.path.exists('/tmp/pylint-server'):
            shutil.rmtree('/tmp/pylint-server')


def load_file(filename):
    """Load file filename and return contents"""
    with open(filename, 'r') as f:
        file_contents = f.read()
    return unicode(file_contents)
