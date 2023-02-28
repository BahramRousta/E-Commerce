from django.views.decorators.cache import cache_page

CACHE_KEY_PREFIX = "home_page"


def cache_view(get_response):

    @cache_page(10, key_prefix=CACHE_KEY_PREFIX)
    def middleware(request):
        response = get_response(request)
        return response

    return middleware