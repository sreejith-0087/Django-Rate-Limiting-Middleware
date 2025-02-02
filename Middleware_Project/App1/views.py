from django.shortcuts import render
from django.core.cache import cache
from django.http import HttpResponse


def count_view(request):
    count = cache.get('count', 0)

    if request.method == 'POST':
        count += 1
        cache.set('count', count, timeout=None)

    return render(request, 'Base.html', {'c': count})

