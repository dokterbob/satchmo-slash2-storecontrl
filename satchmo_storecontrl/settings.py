from django.conf import settings

SLASH2_API_ENDPOINT = getattr(settings, 'SLASH2_API_ENDPOINT', 'http://scdb.slash2.nl/api/sc_webshop_new/soap.wsdl')
SLASH2_QUERY_LIMIT = getattr(settings, 'SLASH2_QUERY_LIMIT', 100)
SLASH2_CREDENTIALS = getattr(settings, 'SLASH2_CREDENTIALS')
