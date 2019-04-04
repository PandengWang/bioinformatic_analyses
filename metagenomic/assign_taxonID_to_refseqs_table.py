#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'Pandeng Wang'
__version__ = '1.0'
__date__ = '2018-01-12'

import sys
import os
import argparse
import re


def parse_refseqs_title(f):
	accid_to_taxonid = {}
	taxName_to_taxonid = {}
	for line in f:
		list = line.strip().split("\t")
		accid_to_taxonid[list[0]] = list[2]
		taxName_to_taxonid[list[3]] = list[2]
	return accid_to_taxonid, taxName_to_taxonid



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "parse nr database title")
	parser.add_argument("-imap", help = "<table> map file of refseqs accession id to taxon id")
	parser.add_argument("-im8", help = "<table> input blast result table")
	parser.add_argument("-o", help="<out> output file")
	
	args = parser.parse_args()
	
	in_map = open(args.imap, "r")
	accid_to_taxonid, taxName_to_taxonid = parse_refseqs_title(in_map)
	in_map.close()
	
	in_m8 = open(args.im8, "r")
	out = open(args.o, "w")
	
	pattern = re.compile(r"ref\|(\w+\.*\d*)\| (.+) \[(.+)\]")
	for line in in_m8:
		if line.startswith("#"):
			pass
		else:
			list = line.strip().split("\t")
			m = re.match(pattern, list[1])
			accid = m.group(1)
			taxname = m.group(3)
			if accid in accid_to_taxonid:
				out.writelines([list[0]+"\t", accid_to_taxonid[accid]+"\t", taxname+"\t", list[1]+"\n"])
			elif taxname in taxName_to_taxonid:
				out.writelines([list[0]+"\t", taxName_to_taxonid[taxname]+"\t", taxname+"\t", list[1]+"\n"])
			else:
				out.writelines([list[0]+"\t", "NA\t", taxname+"\t", list[1]+"\n"])
		
	in_m8.close()
	out.close()
