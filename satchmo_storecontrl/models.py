# Apparently this is the best place to connect to signals
# Ref: http://stackoverflow.com/questions/2095155/django-app-initalization-code-like-connecting-to-signals


import logging
logger = logging.getLogger('satchmo_storecontrl')

from satchmo_store.shop import signals

from satchmo_storecontrl.listeners import *

logger.debug('Connecting storecontrol push_order function to order_success signal.')
signals.order_success.connect(push_order)

