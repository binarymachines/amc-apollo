#!/usr/bin/env python

'''Usage:
            ngst --config <configfile> --target <target_datastore> [--datafile <datafile>] [--limit=<max_records>]           
            ngst --config <configfile> --list-targets

   Options:            
            -i --interactive   Start up in interactive mode
'''

#
# ngst: command line utility for pushing extracted records into a Mercury data pipeline
#


import docopt
from docopt import docopt as docopt_func
from docopt import DocoptExit
import os, sys
import csv
import json
from snap import snap, common
import datamap as dmap
import yaml
import logging


def main(args):
    print(common.jsonpretty(args))

    limit = -1
    if args.get('--limit') is not None:
        limit = int(args['--limit'])
    list_mode = False
    stream_input_mode = False

    if args['--target'] == True and args['<datafile>'] is None:
        print('Streaming mode enabled.')
        record_count = 0
        while True:
            if record_count == limit:
                break
            raw_line = sys.stdin.readline()
            line = raw_line.lstrip().rstrip()
            if not len(line):
                break            
            record_count += 1
            print('read record #%s from standard input.' % record_count)
    elif args['<datafile>']:
        input_file = args['<datafile>']
        print('File input mode enabled. Reading from input file %s...' % input_file)
        record_count = 0
        with open(input_file) as f:
            for line in file:
                if record_count == limit:
                    break

                
                record_count += 1

if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    main(args)



