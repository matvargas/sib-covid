# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse


def home(request):
      return render(
        request,
        'covid_data_viewer/home.html',
      )

def supported_datasets(request):
      return render(
        request,
        'covid_data_viewer/supported_datasets.html',
      )

def about_data(request):
      return render(
        request,
        'covid_data_viewer/about_data.html',
      )

def view(request):
      return render(
        request,
        'covid_data_viewer/view.html',
      )

def contact(request):
      return render(
        request,
        'covid_data_viewer/contact.html',
      )