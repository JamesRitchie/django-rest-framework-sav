# Session Authentication View for Django Rest Framework

[![Build Status](https://travis-ci.org/JamesRitchie/django-rest-framework-sav.svg?branch=master)](https://travis-ci.org/JamesRitchie/django-rest-framework-sav)
[![Coverage Status](https://coveralls.io/repos/JamesRitchie/django-rest-framework-sav/badge.svg?branch=master)](https://coveralls.io/r/JamesRitchie/django-rest-framework-sav?branch=master)
[![Code Health](https://landscape.io/github/JamesRitchie/django-rest-framework-sav/master/landscape.svg?style=flat)](https://landscape.io/github/JamesRitchie/django-rest-framework-sav/master)
[![PyPI version](https://badge.fury.io/py/djangorestframework_sav.svg)](http://badge.fury.io/py/djangorestframework_sav)

This package extends Django Rest Framework to add a Session Authentication view
, in a similar manner to the `obtain_auth_token` view.
It allows session login and logout in a REST-like manner, ideal if you want to
completely decouple a single-page application from your backend.

Whilst the package is quite simple, providing one view and reusing the
[serializer](https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/authtoken/serializers.py)
from the included `auth_token` app, it is well tested, making it useful for
production systems using Django Rest Framework 3.0.
The build matrix for testing covers all currently supported versions of Django
and their compatible Python versions.

## Installation

Grab the package using PIP.

```zsh
pip install djangorestframework-sav
```

Add `rest_framework_sav` to `INSTALLED_APPS` in `settings.py`.

```python
INSTALLED_APPS = [
    ...
    'rest_framework_sav',
    ...
]
```

Make sure
[Session Authentication](http://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication)
is setup correctly.

In your URLconf, add the view to the endpoint you want it at.

```python
from rest_framework_sav.views import session_auth_view

urlpatterns += [
    url(r'^auth-session/$', session_auth_view)
]
```

In production, make sure to serve this view only over HTTPS.

## Usage

To login, send a POST request with `username` and `password` fields to the
endpoint.
Successful attempts will return with HTTP status 200, and a JSON message in the
response body.

```json
{'detail': 'Session login successful.'}
```

The view will call Django's
[`login`](https://docs.djangoproject.com/en/1.7/topics/auth/default/#django.contrib.auth.login)
method if it passes the
[`authenticate`](https://docs.djangoproject.com/en/1.7/topics/auth/default/#django.contrib.auth.authenticate) method, setting the session cookie on the client, and providing a CSRF token.
Unsuccessful attempts will return with HTTP status 400, and a JSON message with
more detail in the response body.

To logout, simply send a DELETE request to the endpoint.
The view will call Django's
[`logout`](https://docs.djangoproject.com/en/1.7/topics/auth/default/#django.contrib.auth.logout)
method, invalidating the current session.
Whilst sending a DELETE request without authenticating will not cause an error,
session authentication must be used in order to have an effect, and this will
require a CSRF token to be sent.

## Future enhancements
 * More informative error status codes other than 400.
 * Implement throttle setting.
