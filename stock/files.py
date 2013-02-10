#!/usr/bin/env python
# encoding: utf-8
"""
files.py

Created by mmiyaji on 2013-02-09.
Copyright (c) 2013  ruhenheim.org. All rights reserved.
"""

import sys, os
from views import *
import simplejson, re, urllib

def upload(request):
    """
    """
    print request.POST, request.FILES
    return HttpResponseRedirect("/upload/")

def main():
    pass

if __name__ == '__main__':
    main()
