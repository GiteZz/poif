def check_if_ok(request):
    if not request.ok:
        print(request.content)
        raise Exception('Request not OK')