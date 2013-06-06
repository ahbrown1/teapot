#!/usr/bin/env python
import sys, logging, time


def hail() :

    logger = logging.getLogger('main')
    ident = 'dunno'
    if len(sys.argv) > 1 :
        ident = sys.argv[1]
    while True :
        logger.info("Hey: %s"%ident)
        time.sleep(5)
     

def main() :

    ''' test; sending output to stdout
    '''
    logger = logging.getLogger('main')
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    hail() 



if __name__ == '__main__' :
   sys.exit(main())
