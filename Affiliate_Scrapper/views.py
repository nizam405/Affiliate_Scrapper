from django.shortcuts import render, redirect

def home(request):
    # template = 'base.html'
    return redirect('project:dashboard')