from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import JsonResponse

from helpers import utils

app = "admin_dashboard/lab_tests/"

@method_decorator(utils.super_admin_only, name='dispatch')
class TestCatalog(View):
    template = app + "test_catalog.html"

    def get(self, request):
        return render(request, self.template)