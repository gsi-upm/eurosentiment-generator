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
            if not 'intype' in myarg:
                myarg['intype'] = 'DIRECT'
            if 'input' in myarg:
                if myarg['intype'] == 'FILE':
                    myarg['document'] = myarg['input']
                elif myarg['intype'] == 'URL':
                    myarg['document_url'] = myarg['input']
        super(TranslationRequestForm, self).__init__(*args, **kwargs)
        self.fields['template'].required = False
        self.fields['template'].empty_label = '- Auto select -'
        self.fields['intype'].required = False

    class Meta:
        model = TranslationRequest
        fields = ['intype', 'document', 'document_url',
                  'informat', 'outformat',
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
                    self.data['informat'] = EuFormat.objects.get(name=self.data['informat']).id
                except:
                    valid = False
                    self._errors['informat'] = ['Not a valid input format',]
        if 'outformat' not in self.data or 'outformat' == '':
            logger.debug('Not a valid output format')
            self._errors['outformat'] = ['Not a valid output format',]
            valid = False
        if 'template' not in self.data or self.data['template'] == "" and valid:
            logger.debug("There is no template ####")
            oformat = self.data['outformat']
            iformat = self.data['informat']
            self.data['template'] = EuTemplate.objects.get(outformat=oformat, informat=iformat).id
        elif 'template' in self.data:
            try:
                if 'informat' not in self.data:
                    self.data['informat'] = EuTemplate.objects.get(pk=self.data['template']).informat.id
                if 'outformat' not in self.data:
                    self.data['outformat'] = EuTemplate.objects.get(pk=self.data['template']).outformat.id
                valid = True
            except:
                logger.debug('Exception in validation')
                valid = False
        if not valid:
            return valid
        # Haven't found a better way to do this. If self._errors is not None,
        # cleaned_data is not generated
        self._errors = None
        return super(TranslationRequestForm, self).is_valid(*args, **kwargs)
