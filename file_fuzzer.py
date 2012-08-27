#!/usr/bin/env python
# encoding: utf-8
__description__ = 'a template based file fuzzer'
__author__ = 'Francisco da Gama Tabanez Ribeiro'
__version__ = '0.1'
__date__ = '2012/03/04'
__license__ = 'GPLv3'

import argparse,os, time

def genrandom(size, forbiddenchars):
	random_buf = os.urandom(size)
	stripped_random_buf = random_buf.strip(''.join(forbiddenchars))
	if(len(forbiddenchars) > 0 and size != len(stripped_random_buf) and any(chr in forbiddenchars for chr in random_buf)):
		stripped_random_buf += os.urandom(size-len(stripped_random_buf))
		stripped_random_buf = random_buf.strip(''.join(forbiddenchars))
	return random_buf

def genfile(filename, data, target_folder):
	if not os.path.exists(target_folder):
		os.makedirs(target_folder)
	tfile=open(target_folder+'/'+filename, 'w')
	tfile.write(data)
	tfile.close()

if __name__ == '__main__':
        parser = argparse.ArgumentParser(description=__description__,epilog='')                   
        parser.add_argument('filename',type=str,help='specify filename for template file')
	parser.add_argument('-d', metavar='bufdata',dest='bufdata',type=str,help='buffer data pattern\t default:A', default='A')
        parser.add_argument('-b', metavar='offsetbegin', default=0, type=int, nargs=1, dest='offsetbegin', help='beginning offset from the multiple targets of fuzzing in the file')
	parser.add_argument('-e', metavar='offsetend', default=-1, type=int, nargs=1, dest='offsetend', help='last offset used for fuzzing the file.\tdefault: -1 (end of file)')
	parser.add_argument('-s', metavar='offsetstepsize', default=[4], type=int, nargs=1, dest='offsetstep', help='offset step used')
        parser.add_argument('-i', metavar='bufminsize', default=4, type=int, nargs=1, dest='bufminsize', help='minimum size for injected buffer')
        parser.add_argument('-t', metavar='dstfilename', type=str, nargs=1, dest='dstfilename', help='destination file name\tdefault is templatefile_offset.templateext')
        parser.add_argument('-n', metavar='dstfiledir', type=str, nargs=1, dest='dstfiledir', help='specifies destination folder for fuzzed files (default: "fuzzed_files")')
	parser.add_argument('-u', metavar='forbiddenchars', type=str, nargs=1, dest='forbiddenchars', help='specifies forbidden chars separated by commas (only makes sense when injecting random buffers)',default='\0')
	parser.add_argument('-a', metavar='bufmaxsize', default=4096, type=int, nargs=1,dest='bufmaxsize', help='maximum size for injected buffer')
        parser.add_argument('-x','-random', dest='bufdatarandom', help='generate random data', required=False, action='store_true')
        parser.add_argument('-w','-wrap', dest='wrap', help='just fuzz the beginning and the end of the file', required=False, action='store_true')

	
        args=parser.parse_args()
       
	print 'opening template file...'
	tfile=open(args.filename,'r')
	templatedata=tfile.read()
	tfile.close()
	
	# default values
	offsetend=len(templatedata)
	offsetbegin=0
	offsetstepsize=4	
	dstfilename=args.filename
	dstfiledir='fuzzed_files'
	forbiddenchars=args.forbiddenchars[0].split(',')
	
	print 'read file %s with length %d' % (args.filename, len(templatedata))
	if args.offsetbegin != 0:
		offsetbegin=args.offsetbegin[0]
	if args.offsetend != -1:
		offsetend=args.offsetend[0]
	if(args.dstfilename is not None):
		dstfilename = args.dstfilename
	if(args.dstfiledir is not None):
		dstfiledir = args.dstfiledir
	if(args.wrap):
		offsetbegin=0
		offsetend=400
		offsetstep=4

	print 'will generate %d files in 5 secs...' % len(range(offsetbegin, offsetend, args.offsetstep[0]))
	time.sleep(5)

	for offset in range(offsetbegin, offsetend, args.offsetstep[0]):
		ffile=''
		ffile+=templatedata[:offset]
		if(args.bufdatarandom):
			ffile+=genrandom(args.bufmaxsize, forbiddenchars)
		else:
			ffile+=args.bufdata*args.bufmaxsize #@TODO: bufdata can only be one char, fix
		ffile+=templatedata[offset:]
		targetfilename=dstfilename.split('.')[0]+'_%.5x.' % offset+dstfilename.split('.')[1]
		genfile(targetfilename, ffile, dstfiledir)
		print 'file: %s generated' % targetfilename

#@TODO: support for file formats with checksum
#@TODO: support for offset hex representation