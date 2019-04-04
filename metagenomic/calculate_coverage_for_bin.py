#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'Pandeng Wang'
__version__ = '1.0'
__date__ = '2018-01-14'

import sys
import os
import argparse
import json


def get_fa_path(dir):
	fa_path = []
	for root, dirs, files in os.walk(dir):
		for file in files:
			fa_path.append(os.path.join(root, file))
	
	return fa_path
	
	
def parse_fa(f):
	scaffold_names = []
	num_scaffold = 0
	total_length = 0
	for line in f:
		if line.startswith(">"):
			num_scaffold += 1
			scaffold_names.append(line.strip().split()[0][1:])
		else:
			total_length += len(line.strip())
	return scaffold_names, num_scaffold, total_length

def parse_rpkm(f):
	f.readline()
	total_reads = f.readline().strip().split()[1]
	info_length_bases = {}
	for line in f:
		if line.startswith("#"):
			pass
		else:
			list = line.strip().split()
			info_length_bases[list[0]] = list[2]
	return info_length_bases, total_reads




def main(args):

	bin_paths = get_fa_path(args.idir)
	
	rpkm_paths = args.irpkm.split(",")
	
	out_title = ["BinID", "# scaffolds", "BinSize (bp)"]
	out_subtitle = ["TotalReads", "NA", "NA"]
	bin_coverage = {}
	
	for bin in bin_paths:
		bin_name = os.path.basename(bin)
		f_bin = open(bin, "r")
		scaffold_names, num_scaffold, total_length = parse_fa(f_bin)
		
		bin_coverage[bin_name] = [bin_name, num_scaffold, total_length]

	
	for rpkm in rpkm_paths:
		# record every sample's name
		out_title.append("mapped_bases_"+os.path.basename(rpkm))
		out_title.append("aveCoverage_"+os.path.basename(rpkm))
		
		f_rpkm = open(rpkm, "r")
		info_length_bases, total_reads = parse_rpkm(f_rpkm)
		
		# record total reads for every sample
		out_subtitle.append(total_reads)
		out_subtitle.append(total_reads)
		
		for bin in bin_paths:
			bin_name = os.path.basename(bin)
			f_bin = open(bin, "r")
			scaffold_names, num_scaffold, total_length = parse_fa(f_bin)
			total_bases = 0
			for scaffold in scaffold_names:
				total_bases += int(info_length_bases[scaffold])
			coverage = float(total_bases) / float(total_length)
			bin_coverage[bin_name].extend([total_bases,coverage])

	out = open(args.o, "w")
	out.writelines(["\t".join(out_title), "\n"])
	out.writelines(["\t".join(out_subtitle), "\n"])
	for key, value in bin_coverage.items():
		out.writelines(["\t".join(map(str, value)), "\n"])
	
	


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "calcualte average coverage for every bin based on rpkm from bbmap")
	parser.add_argument("-irpkm", type=str, help = "<str> name of rpkm files, can be more than one but seperated by ','")
	parser.add_argument("-idir", type=str, help = "<dir> name of dir which contain bin fasta files")
	parser.add_argument("-o", type=str, default="bin_coverage.tsv",help="<str> name of output file")
	
	args = parser.parse_args()
	
	main(args)