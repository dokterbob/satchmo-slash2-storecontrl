from django_extensions.management.jobs import HourlyJob

from satchmo_storecontrl.sync import StockManager

class Job(HourlyJob):
    help = "Synchronise stock with Slash2 SOAP server."

    def execute(self):
        s = StockManager()
        s.sync_stock()
