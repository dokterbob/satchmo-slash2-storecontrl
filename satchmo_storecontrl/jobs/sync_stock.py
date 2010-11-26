import logging

logger = logging.getLogger(__name__)

from django_extensions.management.jobs import BaseJob

from satchmo_storecontrl.settings import *

class Job(BaseJob):
    help = "Synchronise stock with Slash2 SOAP server."

    def execute(self):
        logger.debug('Running stupid job.')