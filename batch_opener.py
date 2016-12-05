#!/usr/bin/env python
# coding: utf-8
#
#
"""Naval Fate.
Usage:
  batch_open.py <prog_name> <fuzz_folder> [--max_proc=<mp>]

Options:
  -h --help     Show this screen.
  --max_proc=<mp>  Speed in knots [default: 3]
  --version     Show version.
"""
from docopt import docopt
import sys, time
from libcall import call

__author__ = 'Francisco Ribeiro <francisco@ironik.org>'
__copyright__ = 'Copyright (c) 2009-2010 Joe Author'
__license__ = 'New-style BSD'
__vcs_id__ = '$Id$'
__version__ = '0.1'

prog_name = sys.argv[0].split('.')[:-1][0]
prog_mode = 'DEBUG'

import logging
logger = logging.getLogger(prog_name)

# create a file handler
handler = logging.FileHandler('%s.log' % prog_name)
console_handler = logging.StreamHandler()

if prog_mode == 'DEBUG':
    logger.setLevel(logging.DEBUG)
    handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)
logger.addHandler(console_handler)

logger.info("%s started" % prog_name)

def isset(var):
    return var in vars() or var in globals()

if sys.version_info >= (2, 7) and sys.version_info < (3,):
    def from_27_until_30():
        pass

def run_process(prog, fuzzfile):
#    logger.info("-> file: %s" % fuzzfile)
    logger.info([prog, fuzzfile])
    proc = call.Command([prog, fuzzfile], 'subprocess', logger=logger, timeout=5)
    proc.start()
    logger.info("stdout: %s\nstderr: %s" % (proc.stdout,proc.stderr))
    logger.info("<- file: %s" % fuzzfile)

def main(prog, filelist, max_processes):
    """Main entry point for the script."""
    #open program max_number_processes
    from multiprocessing import Pool
    import subprocess

        # Start a Pool with <number_of_processes>
    pool = Pool(processes=max_processes)
    jobs = []

    for fuzzfile in filelist:
        # Run the function
#        logger.debug("adding file: %s" % fuzzfile)
        proc = pool.apply_async(func=run_process, args=(prog,fuzzfile ))
        jobs.append(proc)

    # Wait for jobs to complete before exiting
    while(not all([p.ready() for p in jobs])):
        time.sleep(5)

    # Safely terminate the pool
    pool.close()
    pool.join()

if __name__ == '__main__':
    arguments = docopt(__doc__, version='proc hypervisor ' + __version__)
    import os
    max_processes = arguments['--max_proc'] # @TODO: determine max CPU
    file_list = os.listdir(arguments['<fuzz_folder>'])
    logger.info("file list loaded with %i files running in %d processes" % (len(file_list), int(max_processes)))
    sys.exit(main(prog = arguments['<prog_name>'], filelist = file_list, max_processes=int(max_processes)))
