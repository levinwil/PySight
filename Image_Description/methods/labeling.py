import json
import logging
import io
import os
import httplib
import urllib2, urllib
from google.cloud import vision
from six.moves import http_client

"""Detects text in the url."""
def detect_text_web(uri):
    vision_client = vision.Client()
    image = vision_client.image(source_uri=uri)
    texts = image.detect_text()
    text = texts[0].description
    return text

"""Detects text in the file located in Google Cloud Storage or on the Web."""
def detect_text(uri):
    uri = "http://s3.amazonaws.com/pisight/" + uri
    vision_client = vision.Client()
    image = vision_client.image(source_uri=uri)
    texts = image.detect_text()
    text = texts[0].description
    return text

"""Gets description of the file located on the web."""
def get_description_web(uri):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '2db33212505b492cb2cf2a417892d932',
    }

    params = urllib.urlencode({
        'visualFeatures': 'Description',
        'language': 'en',
    })

    body = "{'url':'" + uri + "'}"
    connection = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    connection.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
    response = connection.getresponse()
    data = json.dumps(response.read()).replace("\\", "")
    description = data.split(":")
    connection.close()
    return description[description.index("[{\"text\"") + 1].split(",")[0].replace("\"", "")

"""Gets description of the file located in Google Cloud Storage or on the Web.
"""
def get_description(uri):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '2db33212505b492cb2cf2a417892d932',
    }

    params = urllib.urlencode({
        'visualFeatures': 'Description',
        'language': 'en',
    })

    body = "{'url':'" +  "http://s3.amazonaws.com/pisight/" + uri + "'}"
    connection = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    connection.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
    response = connection.getresponse()
    data = json.dumps(response.read()).replace("\\", "")
    description = data.split(":")
    connection.close()
    return description[description.index("[{\"text\"") + 1].split(",")[0].replace("\"", "")
