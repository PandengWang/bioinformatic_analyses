#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'Pandeng Wang'
__version__ = '1.0'
__date__ = '2018-01-13'

import sys
import os
import argparse


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "parse silva database title")
	parser.add_argument("-i", help = "<fasta> input silva file")
	parser.add_argument("-o", help="<out> output file")
	
	args = parser.parse_args()
	
	in_fa = open(args.i, "r")
	out = open(args.o, "w")
	
	

	for line in in_fa:
		if line.startswith(">"):
			list = line.strip().split()
			id = list[0][1:]
			taxon = " ".join(list[1:])
			out.writelines([id+"\t",taxon+"\n"])
		else:
			pass
	in_fa.close()
	out.close()
