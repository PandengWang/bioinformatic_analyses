#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'Pandeng Wang'
__version__ = '1.0'
__date__ = '2018-01-12'

import sys
import os
import argparse


def parse_map_title(f):
	id_to_name = {}
	for line in f:
		list = line.strip().split("\t")
		id_to_name[list[0]] = "\t".join(list[1:])
	
	return id_to_name



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "assign gene name to every geneID in coverage table (LJL)")
	parser.add_argument("-imap", help = "<table> input map file")
	parser.add_argument("-icov", help = "<table> input coverage table")
	parser.add_argument("-o", help="<out> output file")
	
	args = parser.parse_args()
	
	in_map = open(args.imap, "r")
	id_to_name = parse_map_title(in_map)
	in_map.close()
	
	in_cov = open(args.icov, "r")
	out = open(args.o, "w")
	
	#header = in_cov.readline()
	#out.write(header)
	for line in in_cov:
		if line.startswith("#"):
			out.writelines([line,])
		else:
		
			line = line.strip()
			list = line.split("\t")
			id = list[0].split("~")[1]
			if id in id_to_name:
				out.writelines([line+"\t", id_to_name[id]+"\n"])
			else:
				out.writelines([line, "\n"])
		
	in_cov.close()
	out.close()
