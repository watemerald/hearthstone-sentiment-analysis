#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place hearthstone_sentiment_analysis data_gathering tests --exclude=__init__.py
black hearthstone_sentiment_analysis data_gathering tests
isort hearthstone_sentiment_analysis data_gathering tests