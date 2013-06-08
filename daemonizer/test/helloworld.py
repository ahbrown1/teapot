#!/usr/bin/env python
import sys, logging, time, os
import argparse

'''
        Example usage:
                daemonizer -f -v info daemonizer.test.helloworld --args '-t HEY --period 5'
'''
def run(argv) :
    '''
      Note run() can be defined with or without an 'argv' parameter
    '''

    logger = logging.getLogger('root')
    logger.setLevel(logging.INFO)
    parser = argparse.ArgumentParser()


    parser.add_argument('-t', '--tag', help='message tag',
                        default='NOTAG' )

    parser.add_argument('-p', '--period', help='rate',
                        default=5 )

    args = parser.parse_args(args=argv)



    count = 0
    ident = os.getpid()
    logger.info("%s: %s"%(__name__, argv))
    while True :
        logger.info("Hey: %s (%d) - %s"%(ident, count, args.tag ))
        count += 1
        time.sleep(int(args.period))
     

if __name__ == "__main__" :
   sys.exit(hail())
