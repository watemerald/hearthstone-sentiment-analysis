#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place hearthstone_sentiment_analysis tests --exclude=__init__.py
black hearthstone_sentiment_analysis tests
isort hearthstone_sentiment_analysis tests