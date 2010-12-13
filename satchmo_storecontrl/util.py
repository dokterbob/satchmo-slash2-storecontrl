import logging

logger = logging.getLogger(__name__)

from suds.client import Client

class Slash2(object):
    """ Object representing the Slash2 API. 
    
    Doctest for the Slash2 object and monkey method.
    
    >>> from satchmo_storecontrl.util import Slash2
    >>> from satchmo_storecontrl.settings import SLASH2_API_ENDPOINT, SLASH2_CREDENTIALS
    >>> s = Slash2(credentials=SLASH2_CREDENTIALS, endpoint=SLASH2_API_ENDPOINT)
    >>> result = s.service.getProductQty(s.credentials, {'limit': 2})
    >>> len(result)
    2
    >>> hasattr(result[0][0][0], 'key')
    True
    >>> hasattr(result[0][0][0], 'value')
    True
    >>> new_result = s._qty_monkey(result)
    >>> new_result[0].has_key('sku')
    True
    >>> new_result[0].has_key('discount')
    True
    >>> new_result[0].has_key('price')
    True
    >>> new_result[0].has_key('cost')
    True
    >>> new_result[0].has_key('qty')
    True
    >>> result = s.getProductQty({'limit': 2})
    >>> result[0].has_key('sku')
    True
    >>> result[0].has_key('discount')
    True
    >>> result[0].has_key('price')
    True
    >>> result[0].has_key('cost')
    True
    >>> result[0].has_key('qty')
    True
    
    """


    def __init__(self, credentials, endpoint):
        c = Client(endpoint)

        self.service = c.service
        self.credentials = credentials
    
    @staticmethod
    def _qty_monkey(results):
        """ Monkey method wrapping API results into something useful. """

        endresult = []
        for item in results:
            try:
                keys = [o.key[0] for o in item[0]]
                values = [o.value[0] for o in item[0]]

                endresult.append(dict(zip(keys, values)))

            except IndexError:
                logging.exception('Monkey failed with IndexError, data was: %s' % item)

        return endresult
            
    
    def __getattr__(self, attr):
        """ Wrap the service's functions nicely in a package. """
        
        if self.__dict__.has_key(attr):
            # The attribute is in the current function
            return self.__dict__[attr]
        
        attr_obj = getattr(self.service, attr, None)
        if attr_obj:
            logger.debug('We can find the current attribute in the service property.')
            # This attribute leads to a SOAP call
            
            if not callable(attr_obj):
                # Our beloved friend is not a callable, simply return the poor
                # fellow.
                logger.debug('The attribute is not a callable, so simply return it.')

                return attr_obj
            
            logger.debug('We\'re wrapping this attribute around!')
            
            def wrapper(*args, **kwargs):
                raw_results = attr_obj(self.credentials, *args, **kwargs)

                if attr == 'getProductQty':
                    return self._qty_monkey(raw_results)
                else:
                    return raw_results
            
            assert callable(wrapper)
            
            return wrapper
        
        raise AttributeError, "'%s' object has no attribute '%s'" % \
            (self.__class__.__name__, str(attr))

def get_slash2():
    logger.debug('Opening connection.') 

    from satchmo_storecontrl.settings import SLASH2_CREDENTIALS, \
                                             SLASH2_API_ENDPOINT

    s = Slash2(credentials=SLASH2_CREDENTIALS, 
               endpoint=SLASH2_API_ENDPOINT)
    
    return s

