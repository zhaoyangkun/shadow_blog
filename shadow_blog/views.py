from django.shortcuts import render


def to_403_html(request, exception, template_name='403.html'):
    return render(request, template_name)


def to_404_html(request, exception, template_name='404.html'):
    return render(request, template_name)


def to_500_html(request, template_name='500.html'):
    return render(request, template_name)
