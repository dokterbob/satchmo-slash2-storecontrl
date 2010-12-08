import logging

logger = logging.getLogger(__name__)

from satchmo_storecontrl.util import get_slash2
from satchmo_storecontrl.settings import SLASH2_CALCULATE_TAX_AUTO, \
                                         SLASH2_TAX_PERCENT


def push_order(sender, order=None, **kwargs):
    """ Push the order back to Slash2. """
    
    assert order, 'Order should not be none.'
    
    logger.debug('Pushing order %s to Slash2.', order)
    
    s = get_slash2()

    # Compose order rules
    order_rules = []
    for item in order.orderitem_set.all():
        product = item.product
        
        order_line = {
            'sku': product.sku,
            'qty': item.quantity
        }
        
        order_rules.append(order_line)

    
    # Concatenate the first and the second line in the address
    address = order.bill_street1
    if order.bill_street2:
        address += "\n%s" % order.bill_street2
    
    # Separate the customers' first and last name
    # The last word in the name is generally the last name
    # Everything before that will become the first name
    # (as this is mainly used for searching anyways)
    name_split = order.bill_addressee.split()
    first_name = ''.join(name_split[:-1])
    last_name = name_split[-1]
    
    
    order_dict = {
        'order_id'                      : order.pk,
        'customer_firstname'            : first_name,
        'customer_lastname'             : last_name,
        # We're not using the addition
        'customer_addition'             : '',
        'customer_update'               : 'update',
        'customer_email'                : order.contact.email,
        'customer_address_street'       : address,
        # This is not nicely defined in Satchmo so we won't use it
        #'customer_address_number'       : '',
        'customer_address_zipcode'      : order.bill_postal_code,
        'customer_address_city'         : order.bill_city,
        #'customer_points'               : '0',
        'customer_address_country'      : '118',
        # This is not in the Satchmo order
        # 'customer_telephone'            : '',
        # 'customer_fax'                  : '',
        # Date defaults to now, which makes sense for now
        #'order_date'                    : "25-12-2011 12:12:12",
        'delivery'                      : 
            {'cost' : order.shipping_cost, 
             'text' : order.shipping_description },
        'order_rules'                   : order_rules,
        # Continue, even when SKU's are not matching
        'continue_order'                : 'true',
        'calculate_tax_auto'            : SLASH2_CALCULATE_TAX_AUTO,
        'tax_percent'                   : SLASH2_TAX_PERCENT,
    }
        
    logger.debug('Sending order to Slash2: %s', order_dict)
    
    # Push order
    #s.pushOrder({'order1': order_dict})
    
    # Check if we have success
    result = s.checkOrderExists(order.pk)
    if result:
        logger.info('Succesfully pushed order %s to Slash2.', order,
                    extra={'data': dict(order_dict=order_dict)})
    else:
        logger.error('Error pushing order %s back to Slash2.', order,
                     extra={'data': dict(order_dict=order_dict)})
    logger.debug('Result of pushing: %s', result)
    

    # """Track inventory and total sold."""
    # # Added to track total sold for each product
    # for item in order.orderitem_set.all():
    #     product = item.product
    #     product.total_sold += item.quantity
    #     if config_value('PRODUCT','TRACK_INVENTORY'):
    #         product.items_in_stock -= item.quantity
    #     product.save()


                                          