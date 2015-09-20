pylint-server
====
[![Build Status](https://travis-ci.org/drivet/pylint-server.svg?branch=master)](https://travis-ci.org/drivet/pylint-server)
[![Coverage Status](https://coveralls.io/repos/drivet/pylint-server/badge.svg?branch=master)](https://coveralls.io/r/drivet/pylint-server?branch=master)
[![Code Climate](https://codeclimate.com/github/drivet/pylint-server/badges/gpa.svg)](https://codeclimate.com/github/drivet/pylint-server)
[![Pylint Rating](https://pylint.desmondrivet.com/drivet/pylint-server/rating.svg)](https://pylint.desmondrivet.com/drivet/pylint-server/report.html)

A small Flask application to keep keep track of pylint reports and ratings
on a per-repository basis.

## Requirements

The two main requirements are Flask and Travis.  No other build server ios
supported at the moment.

## Deployment and Usage

This application configures a POST route on /reports.  This endpoint accepts
a pylint report generated from your travis build, and a travis job id.

In your install section, put something like the following:

<pre>
install:
  - "pip install pylint"
</pre>

In your after_success section, put something like this:

<pre>
after_success:
  - pylint --output-format=html pylint_server > /tmp/pylint-report.html
  - curl -v -m 120 -X POST -F travis-job-id=$TRAVIS_JOB_ID -F pylint-report=@/tmp/pylint-report.html https://pylint.whatever.com/reports
</pre>

Assuming you're using github, the app will deposit the report under:

<pre>
/githubuser/repo/report.html
</pre>

And a colour coded pylint rating image under:

<pre>
/githubuser/repo/rating.svg
</pre>

Put a badge on your README accordingly.
