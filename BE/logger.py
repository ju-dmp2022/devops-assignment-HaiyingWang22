import sys
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

def get_logger(name) -> logging.Logger:
    '''
        Creates a logger for logging to stdout and Azure Appliction Insights...
    '''
    logger = logging.getLogger(name)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)

    azure_handler = AzureLogHandler(connection_string="InstrumentationKey=8f7163cd-5d09-4686-90b1-d428b5ac9544;IngestionEndpoint=https://northeurope-2.in.applicationinsights.azure.com/;LiveEndpoint=https://northeurope.livediagnostics.monitor.azure.com/;ApplicationId=2a194e7e-1d49-4bd7-a3d4-01aef5afd02c")
    azure_handler.setFormatter(logging.Formatter('%(funcName)s'))
    logger.addHandler(azure_handler)
    logger.setLevel(logging.DEBUG)
    return logger