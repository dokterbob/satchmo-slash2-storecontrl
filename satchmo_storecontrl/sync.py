import logging

logger = logging.getLogger(__name__)

from decimal import Decimal

from satchmo_storecontrl.settings import SLASH2_QUERY_LIMIT, \
                                         SLASH2_DEBUG_MODE, \
                                         SLASH2_FETCH_ALL, \
                                         SLASH2_REMOVE_UNMATCHED

from satchmo_storecontrl.util import get_slash2

from product.models import Product


class StockManager(object):
    """ Wrapper object for stock management functions """
    
    def __init__(self, slash2=None):
        if slash2:
            self.slash2 = slash2
        else:
            self.slash2 = get_slash2()

    @staticmethod
    def get_product_by_sku(sku):
        try:
            product = Product.objects.get(sku__contains=sku)

            logger.debug('Product found', extra={'data': dict(sku=sku)})
        
            return product

        except Product.DoesNotExist:
            logger.info('Product not found', extra={'data': dict(sku=sku)})
        
            return None
    
    @classmethod
    def update_sku_qty(cls, sku, qty):
        """ Updates the QTY for a given SKU, if available. """
    
        if qty != None:
            logger.debug('Updating SKU',
                         extra={'data': dict(sku=sku,
                                             stock=qty)})
    
            product = cls.get_product_by_sku(sku)

            if product:

                product.items_in_stock = Decimal(qty)
                product.save()
        
                logger.info('Stock updated and saved', 
                    extra={'data': dict(sku=sku, qty=qty, product=product)})
       
                return True
        
        else:
            logger.info('No stock quantity for SKU',
                        extra={'data': dict(sku=sku)})
        
        return False
    
    def update_products(self, products, fetch_all):
        logger.debug('%d products returned.', len(products))        

        success_list = []

        for product in products:            
            success = self.update_sku_qty(product['sku'].strip(), product['qty'])
                
            if success or SLASH2_REMOVE_UNMATCHED:
                # Remove the SKU's which have been processed, if any have been processed at all
                if SLASH2_DEBUG_MODE:
                    logger.info('Not removing updated articles from buffer - debug mode.')
                else:
                    if not fetch_all:
                        success = self.slash2.removeSkuFromBuffer([product['sku'],])

                        if success:
                            logger.debug('Removed updated SKU\'s from buffer')
                        else:
                            logger.warning('Error removing SKU\'s from buffer')

    def sync_stock(self, fetch_all=SLASH2_FETCH_ALL):
        logger.debug('Fetching max. %d updated products.', SLASH2_QUERY_LIMIT)

        options = {'limit': SLASH2_QUERY_LIMIT}

        if fetch_all:
            options.update({'useBuffer': False,
                            'offset': 0 })

            logger.debug('Fetching in buffer mode')

            more_items = True
            while more_items:
                products = self.slash2.getProductQty(options)

                self.update_products(products)

                options['offset'] += SLASH2_QUERY_LIMIT

                if len(products) < SLASH2_QUERY_LIMIT:
                    more_items = False
                    logger.debug('Finished lookup, bailing out')
                else:
                    logger.debug('There is more to find here.')
        else:
            products = self.slash2.getProductQty(options)

            # If buffer mode is not used, we can only do a single round
            self.update_products(products, fetch_all)
