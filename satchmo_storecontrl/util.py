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
    def doofus(obj):
        """ Doofus prevents IndexErrors from happening where they should not. He
            is a big friend of Monkey.
        """
        
        try:
            return obj[0]
    
        except IndexError:
        
            logging.debug('Invalid data in Monkey. Exception prevented.')
            return [] 


    @staticmethod
    def _qty_monkey(results):
        """ Monkey method wrapping API results into something useful. """
                
        endresult = []
        for item in results:
            try:
                keys = [Slash2.doofus(o.key) for o in item[0]]
                

                values = [Slash2.doofus(o.value) for o in item[0]]

                endresult.append(dict(zip(keys, values)))

            except Exception:
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

countries = \
    {'AD': '3',
     'AE': '182',
     'AG': '5',
     'AL': '1',
     'AM': '7',
     'AO': '4',
     'AR': '6',
     'AT': '131',
     'AU': '8',
     'AZ': '9',
     'BA': '19',
     'BB': '13',
     'BD': '12',
     'BE': '14',
     'BF': '24',
     'BG': '23',
     'BH': '11',
     'BI': '25',
     'BJ': '16',
     'BN': '22',
     'BR': '21',
     'BT': '17',
     'BW': '20',
     'BY': '186',
     'BZ': '15',
     'CA': '27',
     'CF': '28',
     'CH': '192',
     'CI': '75',
     'CL': '29',
     'CM': '81',
     'CN': '30',
     'CO': '31',
     'CR': '35',
     'CU': '36',
     'CV': '80',
     'CY': '37',
     'CZ': '173',
     'DE': '42',
     'DJ': '39',
     'DK': '38',
     'DM': '40',
     'DO': '41',
     'DZ': '2',
     'EC': '43',
     'EE': '48',
     'EG': '44',
     'ER': '47',
     'ES': '160',
     'ET': '49',
     'FI': '52',
     'FJ': '50',
     'FM': '109',
     'FR': '53',
     'GA': '54',
     'GB': '183',
     'GD': '58',
     'GE': '56',
     'GH': '57',
     'GM': '55',
     'GN': '61',
     'GQ': '46',
     'GR': '59',
     'GT': '60',
     'GW': '62',
     'GY': '63',
     'HN': '65',
     'HR': '87',
     'HT': '64',
     'HU': '66',
     'ID': '70',
     'IE': '67',
     'IL': '73',
     'IN': '69',
     'IQ': '71',
     'IR': '72',
     'IS': '68',
     'IT': '74',
     'JM': '76',
     'JO': '79',
     'JP': '77',
     'KE': '83',
     'KG': '84',
     'KH': '26',
     'KI': '85',
     'KN': '144',
     'KP': '124',
     'KR': '190',
     'KW': '86',
     'KZ': '82',
     'LB': '91',
     'LI': '94',
     'LK': '161',
     'LR': '92',
     'LS': '89',
     'LT': '95',
     'LU': '96',
     'LV': '90',
     'LY': '93',
     'MA': '104',
     'MC': '111',
     'ME': '113',
     'MG': '98',
     'MH': '105',
     'MK': '97',
     'ML': '102',
     'MM': '115',
     'MN': '112',
     'MR': '106',
     'MT': '103',
     'MU': '107',
     'MV': '100',
     'MW': '99',
     'MX': '108',
     'MY': '101',
     'MZ': '114',
     'NA': '116',
     'NE': '122',
     'NG': '123',
     'NI': '120',
     'NL': '118',
     'NO': '125',
     'NP': '119',
     'NR': '117',
     'NZ': '121',
     'OM': '129',
     'PA': '134',
     'PE': '137',
     'PG': '135',
     'PH': '51',
     'PK': '132',
     'PL': '138',
     'PT': '139',
     'PW': '133',
     'PY': '136',
     'QA': '140',
     'RO': '141',
     'RS': '153',
     'RU': '142',
     'RW': '143',
     'SA': '150',
     'SB': '147',
     'SC': '154',
     'SD': '162',
     'SE': '191',
     'SG': '156',
     'SI': '157',
     'SL': '155',
     'SM': '149',
     'SN': '152',
     'SO': '159',
     'SR': '163',
     'ST': '151',
     'SV': '45',
     'SY': '165',
     'SZ': '164',
     'TD': '172',
     'TG': '169',
     'TH': '168',
     'TJ': '166',
     'TL': '130',
     'TM': '176',
     'TN': '174',
     'TO': '170',
     'TR': '175',
     'TT': '171',
     'TV': '177',
     'TW': '193',
     'TZ': '167',
     'UA': '127',
     'UG': '126',
     'US': '184',
     'UY': '178',
     'UZ': '128',
     'VA': '180',
     'VC': '146',
     'VN': '185',
     'VU': '179',
     'WS': '148',
     'YE': '78',
     'ZA': '189',
     'ZM': '187',
     'ZW': '188'}
