![GSI Logo](http://gsi.dit.upm.es/templates/jgsi/images/logo.png)
[Marl Generator](http://demos.gsi.dit.upm.es/eurosentiment/marlgenerator) 
==================================

Introduction
---------------------
This tool will take several input formats and translates them to the [Marl](http://gsi.dit.upm.es/ontologies/marl) format.

Marl Generator is under heavy development. As of this writing, it supports:

* Creating and administrating translation templates (admin level)
* Editing templates to convert traditional formats (csv, tsv, xls) formats to Marl
* Using the available templates to translate known formats through this portal or via POST requests
* Saving or outputting the result

In the future, we might include the following features:
* Conversion of semantic formats
* Automatic translation between semantic formats (e.g. [RDF](http://www.w3.org/RDF/) to [JSON-LD](http://json-ld.org/))
* Auto selection of the best template based on the input format


Installation instructions
------------------------------
This repository contains all the code necessary to run a marlgenerator. To install it, follow the following steps:

* Copy the eurosentiment/settings.py.template to eurosentiment/settings.py
* Add your database information to settings.py
* Create a virtualenv (preferably, in the project root)
* Install the required packages:

    pip install -r requirements.txt

* Test the environment with:

    python manage.py runserver localhost:<PORT>


If the standalone server works, you can try serving the portal via apache/nginx and WSGI. It has been tested with apache2 and uwsgi. In that case you will also need to serve the static files from your web server. An example configuration for Apache2 would be:

```
<VirtualHost *:80>

    [ ... ]

    WSGIScriptAlias /eurosentiment /path_to_eurosentiment/eurosentiment/wsgi.py
    WSGIDaemonProcess eurosentiment user=www-data group=www-data processes=nprocesses threads=nthreads python-path=/path_to_eurosentiment:/path_to_eurosentiment/venv/lib/python2.7/site-packages
    WSGIProcessGroup eurosentiment
    <Directory /path_to_eurosentiment>
    Order allow,deny
    Allow from all
    </Directory>

    Alias /eurosentiment/robots.txt /path_to_eurosentiment/static/robots.txt
    Alias /eurosentiment/favicon.ico /path_to_eurosentiment/static/favicon.ico

    AliasMatch ^eurosentiment/([^/]*\.css) /path_to_eurosentiment/static/styles/$1

    Alias /eurosentiment/media/ /path_to_eurosentiment/media/
    Alias /eurosentiment/static/ /path_to_eurosentiment/static/

    <Directory /path_to_eurosentiment/static>
    Order deny,allow
    Allow from all
    Options -Indexes
    </Directory>

    <Directory /path_to_eurosentiment/media>
    Order deny,allow
    Allow from all
    Options -Indexes
    </Directory>

</VirtualHost>
```

Acknowledgement
---------------
EUROSENTIMENT PROJECT
Grant Agreement no: 296277
Starting date: 01/09/2012
Project duration: 24 months

![Eurosentiment Logo](http://eurosentiment.eu/wp-content/themes/twentyten/images/logo_grande.png)
![FP7 logo](http://eurosentiment.eu/wp-content/themes/twentyten/images/xlogo_fp7.gif.pagespeed.ic.9J-_8W8AHX.png)
