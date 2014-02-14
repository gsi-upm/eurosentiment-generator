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


from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime, date
from django_languages.fields import LanguageField

OUTFORMATS = (
    ('jsonld', 'JSON-LD'),
    ('rdf', 'RDF+XML'),
    ('nt', 'N-Triples'),
    ('trix', 'TRIX'),
)

def validate_name(name):
    valid = True
    try:
        name.encode('ascii')
    except UnicodeEncodeError:
        valid = False
    if not valid:
        raise ValidationError('Choose a name with ascii characters, without spaces')
    return valid


class EuFormat(models.Model):
    CSV = 'csv'
    TSV = 'tsv'
    ODS = 'ods'
    XLS = 'xls'
    JSONLD = 'jsonld'
    XML = 'xml'
    fileformats = ((CSV, 'csv - Comma Separated Values'),
                   (TSV, 'tsv - Tab Separated Values'),
                   (ODS, 'ods - Open Document Spreadsheet'),
                   (XLS, 'xls - Microsoft Excel Spreadsheet'),
                   (JSONLD, 'json-ld - JSON for Linked Data'),
                   (XML, 'XML - XML format')
                    )
    name = models.CharField('Format name', max_length=200, unique=True)
    extension = models.CharField('File extension', max_length=10, choices=fileformats, default=CSV)
    mimetype = models.CharField('MIME type', max_length=25, default='text/plain')
    description = models.TextField('Description of the format', max_length=200)
    example = models.FileField('Example of the format', upload_to='examples', blank=True)
    usedTimes = models.IntegerField('Times it has been used', default=0, editable=False)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = "File Format"


class EuTemplate(models.Model):
    name = models.CharField('Template name', max_length=200, validators=[validate_name], unique=True)
    text = models.TextField('Template')
    informat = models.ForeignKey(EuFormat, related_name='templateinput', verbose_name='Input format')
    outformat = models.CharField(max_length=10, choices=OUTFORMATS, verbose_name='Output format')
    usedTimes = models.IntegerField('Times it has been used', default=0, editable=False)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = "Conversion Template"


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^django_languages\.fields\.LanguageField"])

class TranslationRequest(models.Model):
    INTYPES = (
        ('DIRECT', 'Direct'),
        ('FILE', 'File'),
        ('URL', 'Specify the file URL'),
    )

    def doc_url(self, filename):
        path = 'documents/%s/%s/%s' % (self.started.strftime("%Y-%m-%d"),
                                       self.ip, filename)
        print 'The path is: %s' % path
        return path

    template = models.ForeignKey(EuTemplate, related_name='request',
                                 verbose_name='Template used')
    document = models.FileField(upload_to=doc_url, blank=True)
    document_url = models.URLField(blank=True)
    intype = models.CharField('Input Type', max_length=10, blank=False,
                              choices=INTYPES, default='FILE')
    informat = models.ForeignKey(EuFormat, related_name='fileinput',
                                 verbose_name='Input format')
    outformat = models.CharField(max_length=10, choices=OUTFORMATS,
                                 verbose_name='output format',
                                 default='JSONLD')
    baseuri = models.CharField('Base URI', max_length=200, blank=True)
    prefix = models.CharField('Prefix', max_length=20, blank=True)
    language = LanguageField('Language of the corpus', blank=True)
    ip = models.GenericIPAddressField('Request IP')
    toFile = models.BooleanField(default=True)
    started = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.started = datetime.now()
        return super(TranslationRequest, self).save(*args, **kwargs)

    def __unicode__(self):
        return 'Request from %s - Template: %s - Input: %s - Output: %s' \
               % (self.ip, self.template, self.informat, self.outformat)
