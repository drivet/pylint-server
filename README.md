# pylint-server

A small Flask application to keep keep track of pylint reports and ratings
on a per-repository basis.

## Requirements

The only real requirement is Flask.  I don't think you need a particularly
up to date one.

## Deployment

This application configures a POST route on /<repo>/github-webhook.

This means that you have to configure your github webhook (in the repo
you're cloning from) to hit your server like this:

http://<yourserver>/<repo>/github-webhook

In any case, what's provides here is mostly a template to be adpated to new
situations.
