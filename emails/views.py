from django.shortcuts import render, render_to_response, get_object_or_404
from django.conf import settings
from models import Email


def show_details(request, eid):
    email = get_object_or_404(Email, pk=eid)
    return render(request, 'emails/details.html', {'email': email})
