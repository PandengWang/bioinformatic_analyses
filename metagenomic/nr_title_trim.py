#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'Pandeng Wang'
__version__ = '1.0'
__date__ = '2018-01-08'

import sys
import os
import argparse


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "Only keep one description for every AA seq")
	parser.add_argument("-i", help = "<txt> input nr title file")
	parser.add_argument("-o", help="<out> output file")
	
	args = parser.parse_args()
	
	in_title = open(args.i, "r")
	out = open(args.o, "w")
	
	

	for line in in_title:
		
		list = line.strip().split("]")
		want = list[0] + "]"
		out.writelines([want,"\n"])
		
		
	in_title.close()
	out.close()
