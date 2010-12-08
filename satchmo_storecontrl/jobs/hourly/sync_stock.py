import logging

logger = logging.getLogger(__name__)

from decimal import Decimal

from django_extensions.management.jobs import HourlyJob

from satchmo_storecontrl.settings import SLASH2_QUERY_LIMIT, \
                                         SLASH2_DEBUG_MODE

from satchmo_storecontrl.util import get_slash2

from product.models import Product


def get_product_by_sku(sku):
    try:
        product = Product.objects.get(sku=sku)

        logger.debug('Product found.', extra={'data': dict(sku=sku)})
        
        return product

    except Product.DoesNotExist:
        logger.info('Product not found.', extra={'data': dict(sku=sku)})
        
        return None

def update_sku_qty(sku, qty):
    """ Updates the QTY for a given SKU, if available. """
    
    product = get_product_by_sku(sku)
    
    if product:
        product.items_in_stock = Decimal(qty)
        product.save()
        
        logger.debug('Stock updated and saved.')
        
        return True
        
    return False
    

class Job(HourlyJob):
    help = "Synchronise stock with Slash2 SOAP server."

    def execute(self):
        s = get_slash2()

        logger.debug('Fetching max. %d updated products.',
                        SLASH2_QUERY_LIMIT)
        
        products = s.getProductQty({'limit': SLASH2_QUERY_LIMIT})
        
        logger.debug('%d products returned.', len(products))        
        
        success_list = []
        
        for product in products:
            logger.debug('Updating SKU',
                         extra={'data': dict(sku=product['sku'],
                                             stock=product['qty'])})
            
            success = update_sku_qty(product['sku'], product['qty'])
                        
            if success:
                # Remove the SKU's which have been processed, if any have been processed at all
                if SLASH2_DEBUG_MODE:
                    logger.info('Not removing updated articles from buffer - debug mode.')
                else:
                
                    success = s.removeSkuFromBuffer([product['sku'],])
        
                    if success:
                        logger.debug('Removed updated SKU\'s from buffer.')
                    else:
                        logging.warning('Error removing SKU\'s from buffer.')
        
        logger.info('Updated stock quantity for %d products.' % len(success_list))
        
