"""
"""

from django.test import TestCase
from django.test import Client

from generator.models import *
from generator.utils import process_document


class SimpleTest(TestCase):
    def setUp(self):
        ignore = EuFormat.objects.create(name="Ignore",
                             extension=EuFormat.TXT,
                             mimetype="text/plain",
                             description="Ignore Everything")
        simple = EuFormat.objects.create(name="Simple",
                             extension=EuFormat.TXT,
                             mimetype="text/plain",
                             description="Simple format")
        EuTemplate.objects.create(name="Ignore to JSONLD",
                          text="Hello World",
                          informat=ignore,
                          outformat="jsonld")
        EuTemplate.objects.create(name="Simple to JSONLD",
                          text="Hello {{ f.read() }}",
                          informat=simple,
                          outformat="jsonld")

    def test_direct_translation_ignore(self):
        """
        """
        c = Client()
        res = c.post("/generator/process", {"intype": "direct",
                                            "text": "Hello",
                                            "informat": "Ignore",
                                            "outformat": "jsonld",
                                            "toFile": "false"})
        self.assertEqual(res.content, "Hello World")

    def test_direct_translation_simple(self):
        """
        """
        c = Client()
        res = c.post("/generator/process", {"intype": "direct",
                                            "text": "Earth",
                                            "informat": "Simple",
                                            "outformat": "jsonld",
                                            "toFile": "false"})
        self.assertEqual(res.content, "Hello Earth")

    def test_file_translation(self):
        """
        """
        with open('/tmp/mike.txt', 'w') as doc:
            doc.write("Mars")
        with open('/tmp/mike.txt', 'r') as doc:
            c = Client()
            res = c.post("/generator/process", {"intype": "file",
                                                "document":  doc,
                                                "informat": "Simple",
                                                "outformat": "jsonld",
                                                "toFile": "false"})
            self.assertEqual(res.content, "Hello Mars")
        with open('/tmp/mike.txt', 'r') as doc:
            c = Client()
            res = c.post("/generator/process", {"intype": "file",
                                                "input":  doc,
                                                "informat": "Simple",
                                                "outformat": "jsonld",
                                                "toFile": "false"})
            self.assertEqual(res.content, "Hello Mars")

    def test_url_translation_simple(self):
        """
        """
        c = Client()
        url = 'http://localhost/eurosentiment/static/test.txt'
        res = c.post("/generator/process", {"intype": "url",
                                            "document_url": url,
                                            "informat": "Simple",
                                            "outformat": "jsonld",
                                            "toFile": "false"})
        self.assertEqual(res.content.strip(), "Hello Test")
