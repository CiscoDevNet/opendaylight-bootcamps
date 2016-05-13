#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright 2015 Cisco Systems, Inc.
# All rights reserved.

from django.http import HttpResponse

def hello(request):
	return HttpResponse("Hello world ! ")