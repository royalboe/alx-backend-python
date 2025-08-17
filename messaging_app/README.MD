# README

## Messaging App

### Filtering

Install django-filter

```bash
pip install django-filter
```

Add django-filter to installed apps

```python
INSTALLED_APPS = [
    ...
    'django_filters',
    ...
]
```

Add filter backend to settings (For global configuration)

```python
REST_FRAMEWORK = {
    ...
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    ...
}
```

### Authentication using JWT

Install django-jwt library

```bash
pip install djangorestframework-simplejwt[crypto]
```

Add JWT authentication to settings

```python
REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        ...
    ),
    ...
}
```

Add jwt to installed apps

```python
INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt',
    ...
]
```
