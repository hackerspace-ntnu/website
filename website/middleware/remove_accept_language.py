class RemoveAcceptLanguageMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.META["HTTP_ACCEPT_LANGUAGE"]:
            del request.META["HTTP_ACCEPT_LANGUAGE"]

        response = self.get_response(request)
        return response
