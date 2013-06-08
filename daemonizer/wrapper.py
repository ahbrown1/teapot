import importlib
import argparse
from daemon.daemon import DaemonContext
import time, string
import lockfile
import sys, logging, time, os
import logging.handlers
import inspect

DFLT_LEVEL = 'WARN'

class ForegroundContext:
        def __enter__(self):
            return None # does nothing

        def __exit__(self, type, value, traceback):
            return True  # does not much more

def wrap() :
    '''
      Run a module inside a daemon.

      * Module (dotted) name passed in on the command line
      * Module must have a run() method as an entry point
    '''

    parser = argparse.ArgumentParser()

    parser.add_argument('module', help='Python run module',)

    parser.add_argument('-f', '--foreground', help='run in foreground',
                         default=False,
                         action="store_true")

    parser.add_argument('-p', '--pidfile', help='PID file path',
                        default=None )

    parser.add_argument('-L', '--lockfile', help='PID file path',
                        default="/var/run/%(prog)s_lock.pid" )

    parser.add_argument('-v', '--verbosity', help='verbosity level',
                        default=DFLT_LEVEL )

    parser.add_argument('-a', '--args', help='quoted module arguments',
                        default=None )

    args = parser.parse_args()

    bad_level = False
    lvl = args.verbosity.upper()
    try :
        level = getattr( logging, lvl ) 
    except AttributeError :
        bad_level = True
        level = getattr( logging, DFLT_LEVEL.upper() ) 
       
    if args.foreground :
        context = ForegroundContext()
    else :
        context = DaemonContext(
                 pidfile=lockfile.FileLock(args.lockfile),
              )

    with context :

        logger = logging.getLogger('root')
        if args.foreground :
            handler = logging.StreamHandler(sys.stdout)
        else :
            handler = logging.handlers.SysLogHandler( address='/dev/log')

        formatter = logging.Formatter('%(levelname)s: %(message)s')
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)

        if bad_level :
            logger.error("Invalid verbosity (%s): defaulted to %s"%(args.verbosity, DFLT_LEVEL))

        prog = os.path.basename(sys.argv[0])
        if  args.pidfile is None :
            if args.foreground :
                pidfile = "./%s.pid"%prog
            else :
                pidfile = "/var/run/%s.pid"%prog
        else :
           pidfile = args.pidfile

        if args.module is None :
            raise Exception("Module name missing")

        try :
            module = importlib.import_module(args.module)
        except Exception as e :
            logger.error("Failed to import module %s : %s"%(args.module, e))
            return 3

        rv = 3

        if  (hasattr( module, 'run' ) and hasattr(module.run, '__call__')):
            try :
                with open( pidfile, 'w' ) as fobj :
                    fobj.write("%s"%os.getpid())

                (_args, varargs, keywords, defaults) = inspect.getargspec(module.run)
                if len(_args) > 0 :
                    #argv = [args.module]
                    argv = []
                    if args.args is not None :
                        argv = string.split(args.args)
    
                    logger.info(argv)

                    rv = module.run(argv)
                else :
                    if args.args is not None :
                       logger.warn('Method [%s.run()] does not take an argument list'%args.module)

                    rv = module.run()

                if rv is None:
                    rv = 0

            except Exception as e:
                    logger.error("Execution failure for %s.run() %s : %s"%(args.module, e))

            finally :
                try:
                    os.unlink(pidfile) 
                except Exception:
                    pass
        else :
            logger.error("Module [%s] does not have a 'run' method"%args.module)
 
        return rv
def main() :
    return( wrap())


if __name__ == '__main__' :
   sys.exit(main())
