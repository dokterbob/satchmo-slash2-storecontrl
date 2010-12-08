from django.conf import settings

SLASH2_API_ENDPOINT = getattr(settings, 'SLASH2_API_ENDPOINT', 'http://scdb.slash2.nl/api/sc_webshop_new/soap.wsdl')
SLASH2_QUERY_LIMIT = getattr(settings, 'SLASH2_QUERY_LIMIT', 100)
SLASH2_CREDENTIALS = getattr(settings, 'SLASH2_CREDENTIALS')
SLASH2_CALCULATE_TAX_AUTO = getattr(settings, 'SLASH2_CALCULATE_TAX_AUTO', 'false')
SLASH2_TAX_PERCENT = getattr(settings, 'SLASH2_TAX_PERCENT', '0')  
SLASH2_CONTINUE_ORDER = getattr(settings, 'SLASH2_CONTINUE_ORDER', 'false')
SLASH2_DEBUG_MODE = getattr(settings, 'SLASH2_DEBUG_MODE', False)
