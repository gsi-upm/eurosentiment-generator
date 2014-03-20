# -*- coding: utf-8 -*-
#  Copyright 2013 J. Fernando Sánchez Rada - Grupo de Sistemas Inteligentes
#                                                 (GSI) DIT, UPM
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


from django.contrib import admin
from codemirror.widgets import CodeMirrorTextarea
from django import forms

from models import EuTemplate, EuFormat, TranslationRequest


class TemplateAdminForm(forms.ModelForm):
    class Meta:
        model = EuTemplate
        widgets = {'text': CodeMirrorTextarea(theme="neat",
                                              attrs={"cols": 10, "max-width": "100px"},
                                              config={'matchBrackets': True,
                                                      'autoCloseBrackets': True,
                                                      'lineWrapping': True})}


class TemplateAdmin(admin.ModelAdmin):
    form = TemplateAdminForm


class RequestAdmin(admin.ModelAdmin):
    readonly_fields = ('document', 'started')
    list_display = ('started', 'template', 'informat', 'outformat', 'ip')
    search_fields = ('started', 'template', 'informat',
                     'outformat', 'ip', 'document')
    list_filter = ('started', 'template', 'informat',
                   'outformat', 'ip', 'document')

admin.site.register(EuTemplate, TemplateAdmin)
admin.site.register(EuFormat)
admin.site.register(TranslationRequest, RequestAdmin)
