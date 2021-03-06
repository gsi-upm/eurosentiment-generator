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

from django import forms
from .models import EuTemplate, EuFormat, TranslationRequest
import logging

logger = logging.getLogger('eurosentiment')

class TranslationRequestForm(forms.ModelForm):
    ALIASES = (
        ('input', 'i'),
        ('informat', 'f'),
        ('intype', 't'),
        ('outformat', 'o'),
        ('base', 'u'),
        ('prefix', 'p'),
        ('language', 'l'),
        ('template', 't')
    )
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        logger.debug('Creating with: ### %s' % repr( args))
        myargs = args
        for myarg in myargs:
            for (arg, alias) in TranslationRequestForm.ALIASES:
                if arg not in myarg and alias in myarg:
                    myarg[arg] = myarg[alias]
        if(len(myargs) > 1):
            nonfiles = myargs[0]
            files = myargs[1]
            logger.debug('Nonfiles: ### %s' % repr(nonfiles))
            if not 'intype' in nonfiles:
                nonfiles['intype'] = 'direct'
            if nonfiles['intype'] == 'file' and 'document' not in files:
                files['document'] = files.get('input', None)
            elif nonfiles['intype'] == 'url' and 'document_url' not in nonfiles:
                nonfiles['document_url'] = nonfiles.get('input', None)
            elif nonfiles['intype'] == 'direct' and 'text' not in nonfiles:
                nonfiles['text'] = nonfiles.get('input', None)
            myargs = (nonfiles, files)
        logger.debug('Using: ### %s' % repr(myargs))
        super(TranslationRequestForm, self).__init__(*myargs, **kwargs)
        self.fields['template'].required = False
        self.fields['template'].empty_label = '- Auto select -'
        self.fields['intype'].required = False
        self.fields['text'].required = False

    class Meta:
        model = TranslationRequest
        fields = ['intype', 'document', 'document_url', 'text',
                  'informat', 'outformat', 'language',
                  'prefix', 'baseuri', 'template', 'toFile']

    def is_valid(self, *args, **kwargs):
        logger.debug('Data: ### %s' % self.data)

        logger.debug('Dir: ### %s' % dir(self))
        valid = True
        self._errors = self._errors if self._errors else {}
        if 'informat' in self.data:
            try:
                int(self.data['informat'])
                EuFormat.objects.get(pk=self.data['informat'])
            except:
                try:
                    logger.debug("Looking for name=%s" %self.data['informat'])
                    logger.debug("Type=%s" %type(self.data['informat']))
                    self.data['informat'] = EuFormat.objects.get(name=self.data['informat'])
                except:
                    valid = False
                    self._errors['informat'] = ['Not a valid input format',]
        if 'outformat' not in self.data or 'outformat' == '':
            logger.debug('Not a valid output format')
            self._errors['outformat'] = ['Not a valid output format',]
            valid = False
        if 'template' not in self.data or self.data['template'] == "" and valid:
            logger.debug("There is no template ####")
            try:
                oformat = self.data['outformat']
                iformat = self.data['informat']
                self.data['template'] = EuTemplate.objects.filter(outformat=oformat, informat=iformat)[0].id
            except:
                self._errors['template'] = ['No template found for intype and outtype',]
                valid = False
        elif 'template' in self.data:
            try:
                self.data['template'] = EuTemplate.objects.get(name=self.data['template']).id
                if 'informat' not in self.data:
                    self.data['informat'] = EuTemplate.objects.get(pk=self.data['template']).informat.name
                if 'outformat' not in self.data:
                    self.data['outformat'] = EuTemplate.objects.get(pk=self.data['template']).outformat
                valid = True
            except Exception as ex:
                self._errors['template'] = ['Invalid template metadata %s' % ex]
                logger.debug('Exception in validation: ', ex)
                valid = False
        if not valid:
            return valid
        # Haven't found a better way to do this. If self._errors is not None,
        # cleaned_data is not generated
        self._errors = None
        return super(TranslationRequestForm, self).is_valid(*args, **kwargs)
