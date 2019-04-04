#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'Pandeng Wang'
__version__ = '1.0'
__date__ = '2018-01-12'

import sys
import os
import argparse


def parse_cov_table(f):
	accid_to_cov = {}
	for line in f:
		list = line.strip().split("\t")
		name = list[0].split()[0]
		accid_to_cov[name] = "\t".join(list[1:])
	
	return accid_to_cov



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "parse nr database title")
	parser.add_argument("-icov", help = "<table> input gene coverage file")
	parser.add_argument("-idia", help = "<table> input diamond result table")
	parser.add_argument("-o", help="<out> output file")
	
	args = parser.parse_args()
	
	in_cov = open(args.icov, "r")
	accid_to_cov = parse_cov_table(in_cov)
	in_cov.close()
	
	in_dia = open(args.idia, "r")
	out = open(args.o, "w")

	for line in in_dia:
		line = line.strip()
		list = line.split("\t")
		if list[0] in accid_to_cov:
			out.writelines([line+"\t", accid_to_cov[list[0]]+"\n"])
		else:
			out.writelines([line, "\n"])
		
	in_dia.close()
	out.close()
