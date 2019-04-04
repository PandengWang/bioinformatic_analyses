#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse


def parse_fa(f):
	'''
	parse fasta file.
	'''
	seqs = {}
	for line in f:
		if line.startswith(">"):
			seq_name = line.strip().split()[0][1:]
			seqs[seq_name] = str()
		else:
			seqs[seq_name] += line.strip()
	return seqs


def parse_m8(f):
	'''
	pasre m8 format table.
	'''
	names = []
	for line in f:
		list = line.strip().split("\t")
		names.append(list[0])
	return names


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "Homework")
	parser.add_argument("-ifa", type =str,help = "<fasta> fasta file you need pick seqs from")
	parser.add_argument("-iname", type=str,help = "<table> the first column must be the seqs name you want to pick")
	parser.add_argument("-o", type=str,help="<fasta> output file")
	
	args = parser.parse_args()
	
	im8 = open(args.iname, "r")
	names = parse_m8(im8)
	im8.close()
	
	ifa = open(args.ifa, "r")
	seqs = parse_fa(ifa)
	ifa.close()
	
	ofile = open(args.o, "w")
	for name in names:
		if name in seqs:
			ofile.writelines([">"+name+"\n", seqs[name]+"\n"])
		else:
			print(name+" is not in fasta file!")

