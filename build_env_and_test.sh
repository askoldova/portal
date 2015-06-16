#!/usr/bin/env bash

pip install -U -r requirements.txt &&
  pip install -U -r requirements_dev.txt &&
  PYTHONPATH=src python src/manage/tests.py test -v 2 --with-coverage --cover-html --cover-html-dir=.coverages

