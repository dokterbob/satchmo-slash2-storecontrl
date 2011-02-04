from django_extensions.management.jobs import DailyJob

from satchmo_storecontrl.sync import StockManager
from satchmo_storecontrl.settings import SLASH2_FETCH_ALL_DAILY


class Job(DailyJob):
    help = "Synchronise full stock with Slash2 SOAP server."

    def execute(self):
        s = StockManager()

        if SLASH2_FETCH_ALL_DAILY:
            s.sync_stock(fetch_all=True)

