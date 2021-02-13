#!/usr/bin/env bash


set -e
set -x

flake8 hearthstone_sentiment_analysis tests
black hearthstone_sentiment_analysis tests --check
isort hearthstone_sentiment_analysis tests --check-only