#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse


__author__ = 'Pandeng Wang'
__version__ = '1.0'
__date__ = '2018-03-16'
__description__='This script is the batch version of split fq based on oligos'


def split_fq(args):
	if os.path.exists(args.odir):
		out_dir = os.path.abspath(args.odir)
	else:
		os.makedirs(args.odir)
		out_dir = args.odir

	all_files = os.listdir(args.idir)
	f_files = []
	r_files = []
	for f in all_files:
		if f.count("forward"):
			f_files.append(f)
		elif f.count("reverse"):
			r_files.append(f)
		else:
			pass
	
	oligos = os.listdir(args.ibdir)

	if len(f_files) == len(r_files) and len(f_files) == len(oligos):
		f_files.sort()
		r_files.sort()
		oligos.sort()
	else:
		print("The number of R1 files , R2 files and oligos files don't match! Please Check it!")
		sys.exit()

	for r1, r2, oligo in zip(f_files, r_files, oligos):
		if r1.split("_")[0] != r2.split("_")[0] or r1.split("_")[0] != oligo.split(".")[0]:
			print("The names of three files don't match each other!")
			sys.exit()
		else:
			pass
			
		ifq1 = os.path.join(args.idir, r1)
		ifq2 = os.path.join(args.idir, r2)
		oligo = os.path.join(args.ibdir, oligo)
		
		if args.t == "bc":
			cmd = 'python3 ~/scripts_16s_its/qc/split_fq_to_sample_by_barcode.py -ifq1 %s -ifq2 %s -bc %s -odir %s -bdiffs %i -blen %i -llen %i' \
			  % (ifq1, ifq2, oligo, args.odir, args.bdiffs, args.blen, args.llen)
		else:
			cmd = 'python3 ~/scripts_16s_its/qc/split_fq_to_sample_by_barcode.py -ifq1 %s -ifq2 %s -oligos %s -odir %s -bdiffs %i -blen %i -llen %i' \
			  % (ifq1, ifq2, oligo, args.odir, args.bdiffs, args.blen, args.llen)
		print("Processing: "+r1+"\t"+r2)
		os.system(cmd)






if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="This script is the batch version of split fq based on oligos file or barcode files")
	
	parser.add_argument("-idir", type=str, help="input dir which contain the fq files")
	parser.add_argument("-t", type=str, choices=["bc", "oligos"],help="the barcode files type", required=True)
	parser.add_argument("-ibdir", type=str, help="input dir which contain files that have barcode info for samples")
	parser.add_argument("-odir", type=str, help="Output: output directory", required=True)
	parser.add_argument("-bdiffs", type=int, default=0, help="Max num of barcode mismatch to be allowed (default:0)")
	parser.add_argument("-blen", type=int, default=12, help="Barcodes length (default:12)")
	parser.add_argument("-llen", type=int, default=2, help="Linker nt length (default:2)")
	
	
	# parse args
	args = parser.parse_args()
	split_fq(args)





