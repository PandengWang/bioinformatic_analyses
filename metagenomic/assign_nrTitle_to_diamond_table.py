#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'Pandeng Wang'
__version__ = '1.0'
__date__ = '2018-01-12'

import sys
import os
import argparse


def parse_nr_title(f):
	accid_to_fun = {}
	for line in f:
		list = line.strip().split("\t")
		accid_to_fun[list[0]] = list[1]
	
	return accid_to_fun



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "parse nr database title")
	parser.add_argument("-inr", help = "<table> input nr title file")
	parser.add_argument("-idia", help = "<table> input diamond result table")
	parser.add_argument("-o", help="<out> output file")
	
	args = parser.parse_args()
	
	in_nr = open(args.inr, "r")
	accid_to_fun = parse_nr_title(in_nr)
	in_nr.close()
	
	in_dia = open(args.idia, "r")
	out = open(args.o, "w")

	for line in in_dia:
		line = line.strip()
		list = line.split("\t")
		if list[1] in accid_to_fun:
			out.writelines([line+"\t", accid_to_fun[list[1]]+"\n"])
		
	in_dia.close()
	out.close()
