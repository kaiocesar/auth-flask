#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import dataset

db = dataset.connect('sqlite:///authflaskdb')
Articles = db['articles']
