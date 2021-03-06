# -*- coding: utf-8 -*-
#    Copyright 2013 J. Fernando Sánchez Rada - Grupo de Sistemas Inteligentes
#                                                       DIT, UPM
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import json
import sys, os

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from models import EuTemplate, EuFormat, TranslationRequest
from .forms import TranslationRequestForm
from utils import *

import logging
logger = logging.getLogger('eurosentiment')


def home(request):
    logger.debug("Home")
    supported = {}
    templates = EuTemplate.objects.all()
    for t in templates:
        supported[t] = {'input': t.informat, 'output': t.outformat}
    logger.debug(supported)
    return render_to_response('home.html', {'supported': supported},
                              RequestContext(request))

def process_home(request):
    form = TranslationRequestForm(initial={'toFile': False})
    return render(request, 'upload.html', {'form': form})

@csrf_exempt
def process(request):
    logger.debug("Processing")
    if request.method == 'POST':
        data = request.POST.copy()
    else:
        data = request.GET.copy()
    logger.debug("Got a Form")
    if "toFile" not in request.POST:
        data["toFile"] = False
    form = TranslationRequestForm(data, request.FILES)
    if form.is_valid():
        logger.debug("Valid form!")
        try:
            logger.debug('Form')
            #logger.debug('Form:%s' % form)
            logger.debug('TheForm')
            req = TranslationRequest()
            logger.debug('Processed')
            req.template = form.cleaned_data['template']
            req.document = form.cleaned_data['document']
            req.document_url = form.cleaned_data['document_url']
            req.text = form.cleaned_data['text']
            req.intype = form.cleaned_data['intype']
            req.informat = form.cleaned_data['informat']
            req.outformat = form.cleaned_data['outformat']
            req.language = form.cleaned_data['language']
            req.toFile = form.cleaned_data['toFile']
            req.ip = get_client_ip(request)
            logger.debug("Got IP")
            req.save()
            return process_document(req, request)
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.debug('Something bad happened in view:')
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.debug(exc_type, fname, exc_tb.tb_lineno)
            logger.debug(ex)
            return HttpResponseBadRequest('Error while processing')
    else:
        field_errors = [(field.label, field.errors) for field in form]
        logger.debug(field_errors)
        logger.error("Invalid Form")
        return HttpResponseBadRequest('Bad form: %s' % json.dumps(field_errors))

def formats(request):
    formats = EuFormat.objects.all()
    templates = EuTemplate.objects.all()
    return render(request, 'formats.html', {'formats': formats, 'templates': templates })

def api(request):
    return render(request, 'api.html', {})
