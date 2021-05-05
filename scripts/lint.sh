#!/usr/bin/env bash


set -e
set -x

flake8 hearthstone_sentiment_analysis data_gathering tests
black hearthstone_sentiment_analysis data_gathering tests --check
isort hearthstone_sentiment_analysis data_gathering tests --check-only