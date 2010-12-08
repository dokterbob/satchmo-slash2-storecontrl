# Apparently this is the best place to connect to signals
# Ref: http://stackoverflow.com/questions/2095155/django-app-initalization-code-like-connecting-to-signals


from satchmo_store.shop import signals

from satchmo_storecontrl.listeners import *

signals.order_success.connect(push_order)

