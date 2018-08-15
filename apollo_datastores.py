#!/usr/bin/env python

import uuid
import json
from collections import namedtuple
from snap import common
from ngst import DataStore
from elasticsearch import Elasticsearch
#from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, connections


ElasticsearchHost = namedtuple('ElasticsearchHost', 'host port')


class KinesisDatastore(DataStore): 
    def __init__(self, service_object_registry, **kwargs):
        DataStore.__init__(self, service_object_registry, **kwargs)
        kwreader = common.KeywordArgReader(*[])
        kwreader.read(**kwargs)
        self.kinesis_svc = service_object_registry.lookup('kinesis')


    def write(self, records, **kwargs):
        for rec in records:
            print('### ready to write record to Kinesis:')
            print('------------------------\n')        
            print(common.jsonpretty(rec))            
            status = self.kinesis_svc.write(rec, 'apollo_test_stream')
            print('Done with status: %s' % status)


class FileStore(DataStore):
    def __init__(self, service_object_registry, **kwargs):
        DataStore.__init__(self, service_object_registry, **kwargs)
        kwreader = common.KeywordArgReader('filename')
        kwreader.read(**kwargs)
        self.filename = kwreader.get_value('filename')        


    def write(self, records, **kwargs):        
        with open(self.filename, 'a') as f:
            for record in records:
                f.write(record)
                f.write('\n')


class ESDatastore(object):
    def __init__(self, service_registry, **kwargs):
        DataStore.__init__(self, service_registry, **kwargs)
        hostname = kwargs.get('hostname')
        port = int(kwargs.get('port', 9200))
        self.esclient = Elasticsearch([{'host': hostname, 'port': port}])
        self.index = kwargs.get('index')
        self.doctype = kwargs.get('doctype')


    def generate_doc_id(self):
        return uuid.uuid4()


    def write(self, recordset, **kwargs):
        for record in recordset:
            self.esclient.index(index=self.index,
                                doc_type=self.doctype,
                                id=self.generate_doc_id(),
                                body=json.loads(record))