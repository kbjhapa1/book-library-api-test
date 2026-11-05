from rest_framework.authentication import SessionAuthentication


class SessionAuthentication401(SessionAuthentication):
    """
    Django REST Framework's stock SessionAuthentication has a quirk:
    when you are NOT logged in, it answers 403 instead of 401.

    By supplying an authenticate_header(), we tell DRF that this scheme can
    "challenge" the client, so DRF answers 401 Unauthorized (plus a
    WWW-Authenticate header).  Result:
        401 = "I don't know who you are"      (authentication problem)
        403 = "I know who you are, but no"    (authorization problem)
    """

    def authenticate_header(self, request):
        return "Session"