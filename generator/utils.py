# -*- coding: utf-8 -*-
#
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


from jinja2 import Environment
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.forms.models import model_to_dict
import json
import xlrd
import sys
import os
from lxml import etree
from datetime import datetime
import requests

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('eurosentiment')


def linesplit(value, separator=' '):
    #print "Received object: %s" % value
    return value.strip().split(separator)


def convertDate(value, informat="%d-%B-%Y", outformat="%Y-%m-%d-"):
    return datetime.strptime(value, informat).strftime(outformat)


def escapejs(val):
        try:
            return json.dumps(val)
        except Exception as ex:
            logger.error(ex)
            return "\"\""


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def download_file(url):
    local_filename = os.path.join(settings.MEDIA_ROOT, url.split('/')[-1])
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:   # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename


def process_document(trans, httprequest):
    logger.debug("PROCESSING!!")
    data = model_to_dict(trans)
    logger.debug("DATA!! %s" % data)
    env = Environment(trim_blocks=True, lstrip_blocks=True, extensions=['jinja2.ext.do',])
    env.globals['linesplit'] = linesplit
    env.globals['convertDate'] = convertDate
    env.globals['len'] = len
    env.filters['escapejs'] = escapejs
    logger.debug('Template: %s - %s' % (type(trans.template.text),
                                        trans.template.text))
    template = env.from_string(trans.template.text)
    iext = trans.informat.extension
    oext = trans.outformat
    if trans.intype == "file":
        logger.debug('file')
        filename = trans.document.path
    elif trans.intype == "url":
        logger.debug('url')
        filename = download_file(trans.document_url)
    else:
        logger.debug('direct')
        filename = os.path.join(settings.MEDIA_ROOT, "direct.%s" % iext )
        idx = 0
        while os.path.isfile(filename):
            idx = idx+1
            filename = os.path.join(settings.MEDIA_ROOT, "direct%s.%s" % (idx, iext ))
        savedfile = open(filename, 'wb')
        savedfile.write(trans.text)

        savedfile.close()
    outputfile = "%s-%s.%s" % (filename.rsplit(iext, 1)[0], "translated", oext)
    logger.debug("######## File: %s" % outputfile)
    if trans.informat.mimetype == 'application/vnd.ms-excel':
        logger.debug('An office file!')
        f = xlrd.open_workbook(filename, on_demand=True)
    elif trans.informat.mimetype == 'application/xml':
        logger.debug('An XML file!')
        f = etree.parse(filename)
    else:
        f = open(filename, 'r')
    data['f'] = f
    logger.debug('pre-stream')
    stream = template.stream(data, filename=filename)
    logger.debug('post-stream')
    if "toFile" in data and data["toFile"]:
        try:
            stream.dump(outputfile)
            #I could do it with array splicing, but it'll
            #be easier to find this in the future
            fname = outputfile.split('/var/www')[1]
            size = os.path.getsize(outputfile)
            accept = httprequest.META.get('HTTP_ACCEPT', 'application/json').split(",")
            if 'text/html' in accept:
                return render(httprequest, 'success.html', {'file': fname})
            else:
                resp = '{"file": "%s", "status": "success", "size": "%s"}' % (fname, size)
                return HttpResponse(resp, mimetype='application/json')
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.debug('Something bad happened during process:')
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.debug('Info: %s %s %s' % (exc_type, fname, exc_tb.tb_lineno))
            logger.debug('Raising')
            raise ex
    logger.debug( "Returning stream")
    return HttpResponse(stream, mimetype="text/plain")
