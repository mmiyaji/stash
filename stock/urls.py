#!/usr/bin/env python
# encoding: utf-8
"""
urls.py

Created by mmiyaji on 2012-11-13.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""
from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from django.conf import settings
import os

urlpatterns = patterns('',
                       url(r'^$', 'stock.general.home', name='home'),
                       url(r'^login/$', 'stock.general.signin'),
                       url(r'^logout/$', 'stock.general.signout'),
                       url(r'^upload/$', 'stock.upload.home', name='upload'),
                       url(r'^archive/$', 'stock.archive.home'),
                       url(r'^archive/author/$', 'stock.archive.authors'),
                       url(r'^archive/author/(?P<author_id>\w+)/$', 'stock.archive.author'),
                       url(r'^archive/year/$', 'stock.archive.years'),
                       url(r'^archive/year/(?P<year>\d+)/$', 'stock.archive.year'),
                       url(r'^entry/$', 'stock.entry.home'),
                       url(r'^entry/(?P<entry_uuid>\w{32})/$', 'stock.entry.detail'),
                       url(r'^entry/(?P<entry_uuid>\w{32})/delete/$', 'stock.entry.delete'),
                       url(r'^entry/(?P<entry_uuid>\w{32})/update/$', 'stock.entry.update'),
                       url(r'^entry/(?P<entry_uuid>\w{32})/rotate/$', 'stock.entry.rotate'),
                       url(r'^author/$', 'stock.author.home'),
                       url(r'^author/meibo/add/$', 'stock.author.meiboadd'),
                       url(r'^author/(?P<author_id>\w+)/$', 'stock.author.detail'),
                       url(r'^author/(?P<author_id>\w+)/update/$', 'stock.author.update'),
                       url(r'^group/$', 'stock.group.home'),
                       url(r'^group/(?P<group_id>\d+)/$', 'stock.group.detail'),
                       url(r'^group/(?P<group_id>\d+)/update/$', 'stock.group.update'),
                       url(r'^group/(?P<group_id>\d+)/delete/$', 'stock.group.delete'),
                       url(r'^group/meibo/add/$', 'stock.group.meiboadd'),
                       url(r'^tag/$', 'stock.tag.home'),
                       url(r'^tag/(?P<tag_id>\d+)/$', 'stock.tag.detail'),
                       url(r'^tag/(?P<tag_id>\d+)/update/$', 'stock.tag.update'),
                       url(r'^tag/(?P<tag_id>\d+)/delete/$', 'stock.tag.delete'),
                       url(r'^tag/meibo/add/$', 'stock.tag.meiboadd'),
                       url(r'^search/$', 'stock.search.home'),
                       url(r'^search/author/$', 'stock.search.author'),
                       )
