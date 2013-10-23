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


from jinja2 import Template, Environment
from django.shortcuts import render
from django.http import HttpResponse
import traceback
import json
import xlrd

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('eurosentiment')

def linesplit(value, separator=' '):
    #print "Received object: %s" % value
    return value.strip().split(separator)


def escapejs(val):
        try:
            return json.dumps(val)
        except Exception as ex:
            logger.error(ex)
            return ""

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def process_document(trans, form, httprequest):
    #import sys
    #reload(sys)
    #sys.setdefaultencoding('utf-8')
    logger.debug("PROCESSING!!")
    env = Environment(trim_blocks=True,lstrip_blocks=True )
    env.globals['linesplit'] = linesplit
    env.filters['escapejs'] = escapejs
    template = env.from_string(trans.template.text)
    filename = trans.document.path
    iext = ".%s" % trans.inputformat.extension
    oext = ".%s" % trans.outputformat.extension
    outputfile = "%s-%s.%s" % (iext.join(filename.rsplit(iext)[:-1]), "translated", oext)
    logger.debug("######## File: %s" % outputfile)
    if trans.inputformat.mimetype == 'application/vnd.ms-excel':
        logger.debug('An office file!')
        f = xlrd.open_workbook(filename, on_demand=True)
    else:
        f = open(filename, 'r')
    stream = template.stream(f=f, filename=filename)
    if "toFile" in form.cleaned_data and form.cleaned_data["toFile"]:
        try:
            stream.dump(outputfile)
            #I could do it with array splicing, but it'll
            #be easier to find this in the future
            fname = outputfile.split('/var/www')[1]
            return render(httprequest, 'success.html', {'file': fname})
        except Exception as ex:
            logger.error('Something bad happened:')
            logger.error(ex)
            raise ex
    return HttpResponse(stream, mimetype="text/html")
