
#!/usr/bin/env python

 
from snap import snap
from snap import core
from snap import common
import json
from snap.loggers import transform_logger as log



def ping_func(input_data, service_objects, **kwargs):
    return core.TransformStatus(json.dumps({'message': 'the SNS listener is alive.'}))


def sns_receive_func(input_data, service_objects, **kwargs):
    log.info(input_data)

    sns_message_raw = input_data['Message']
    log.info(sns_message_raw)

    sns_message = json.loads(sns_message_raw)
    print(common.jsonpretty(sns_message))

    s3_segment = sns_message['Records'][0]['s3']

    keyname = s3_segment['object']['key']

    s3_svc = service_objects.lookup('s3')
    file_loc = s3_svc.download_object('datalab.mercury', keyname)
    log.info('### Downloaded S3 object to  %s.' % file_loc)
    
    return core.TransformStatus(json.dumps({}))



