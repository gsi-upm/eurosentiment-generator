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

from django.forms import ModelForm, Form, ModelChoiceField, FileField, BooleanField
from .models import EuTemplate


class TranslationRequestForm(Form):
    template = ModelChoiceField(queryset=EuTemplate.objects.all(),
                                to_field_name='name')
    document = FileField()
    toFile = BooleanField(initial=True, required=False, label="Save to file")

    #class Meta:
        #model = TranslationRequest
        #fields = ['template', 'document']

    def is_valid(self):
        print "Is valid form??"
        super(TranslationRequestForm, self).is_valid()
        cd = self.cleaned_data
        print "Cleaned data"
        #return "template" in cd and cd["template"] and \
               #"document" in cd and cd["document"]
        return True
