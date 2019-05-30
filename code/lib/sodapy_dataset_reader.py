#sodapy_dataset_reader
#this file contains classes that use the 
#  sodapy library https://pypi.org/project/sodapy/
#  to interface with the Socrata API https://dev.socrata.com
#
# Many open data platforms are implemented using this API
#
# The SodapyDomainExporer provides a method to return the 
#   datasets for a specified domain. (May time out if too many.)
# 
# The SodapyDatasetReader class instantiates
#   a reader for the given domain, and stores the 
#   metadata in a class variable.
#  class allows you to instantiate the reader using 
#   the domain source name.


import pandas as pd
from sodapy import Socrata
import warnings

class SodapyDomainExplorer():


    def __init__(self, source_domain):
        #my identification
        my_app_token = 'IWXpLDTFN6TveJtORQ2vc0qj5'
        my_user_name = 'annetkerr@gmail.com'
        my_password = ';6L8vBSpTJ66'
        self.datasource_domain = source_domain
        self.client = Socrata(self.datasource_domain,
                my_app_token,
                my_user_name,
                my_password)

    def get_datasets(self):
        return (self.client.datasets())


class SodapyDatasetReader():

    #instntiate the class be establishing a client with the source domain
    def __init__(self, source_domain, dataset_id):
        #my identification
        my_app_token = 'IWXpLDTFN6TveJtORQ2vc0qj5'
        my_user_name = 'annetkerr@gmail.com'
        my_password = ';6L8vBSpTJ66'
        self.datasource_domain = source_domain
        self.dataset_id = dataset_id
        self.client = Socrata(self.datasource_domain,
                my_app_token,
                my_user_name,
                my_password)
        self.md = self.client.get_metadata(self.dataset_id)

    #read a dataset from the source domain and return a dataframe
    def get_df(self, limit=1000, filter=None):     
        if not filter == None:
            self.filter = filter
            self.results = self.client.get(self.dataset_id, where=filter, limit=limit)
        else:
            self.results = self.client.get(self.dataset_id, limit=limit)
        self.df = pd.DataFrame.from_records(self.results)
        return(self.df)

    def get_metadata(self):
        return(self.md)

    def get_row_count(self):
        return(self.client.get(self.dataset_id, query='select count(*)'))
