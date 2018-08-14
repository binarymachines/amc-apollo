#!/usr/bin/env python

import json
from snap.loggers import request_logger as log


def decode_application_json(http_request):
    log.info('>>> Invoking custom request decoder.')
    decoder_output = {}
    decoder_output.update(http_request.get_json(silent=True))
    return decoder_output

def decode_text_plain(http_request):
    if not len(http_request.data):
        return {}
    return json.loads(http_request.data.decode())


def decode_text_plain_utf8(http_request):
    if not len(http_request.data):
        return {}
    return json.loads(http_request.data.decode())
