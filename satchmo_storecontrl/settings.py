from django.conf import settings

SLASH2_API_ENDPOINT = getattr(settings, 'SLASH2_API_ENDPOINT', 'http://scdb.slash2.nl/api/sc_webshop_new/soap.wsdl')
""" URL of the Slash2 SOAP API endpoint. """

SLASH2_QUERY_LIMIT = getattr(settings, 'SLASH2_QUERY_LIMIT', 100)
""" Maximum number of stock items retreived in a batch query. """

SLASH2_CREDENTIALS = getattr(settings, 'SLASH2_CREDENTIALS')
""" Credentials for logging into the Slash2 API. """

SLASH2_CALCULATE_TAX_AUTO = getattr(settings, 'SLASH2_CALCULATE_TAX_AUTO', 'false')
""" Badly documented tax auto setting. Better leave this as it is or call
    Slash2 about it.
"""

SLASH2_TAX_PERCENT = getattr(settings, 'SLASH2_TAX_PERCENT', '0')
""" Tax percentage used. Please refer to the previous setting. """

SLASH2_CONTINUE_ORDER = getattr(settings, 'SLASH2_CONTINUE_ORDER', 'false')
""" Whether or not to continue orders for products with unknown SKU's. """

SLASH2_DEBUG_MODE = getattr(settings, 'SLASH2_DEBUG_MODE', False)
""" In debug mode, no products are removed from the buffer when not working
    in ALL mode.
"""

SLASH2_FETCH_ALL = getattr(settings, 'SLASH2_FETCH_ALL', False)
""" If this is False, only updated items are returned by the Slash2 API.
    When True, all items in the system are returned.
"""

SLASH2_REMOVE_UNMATCHED = getattr(settings, 'SLASH2_REMOVE_UNMATCHED', False)
""" Remove unmatched products from bugger"""
