#!/bin/usr/env python3
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import JSONParser
import io


def parseBody(body):
    stream = io.BytesIO(body)
    data = JSONParser().parse(stream)
    return data

