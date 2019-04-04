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
	fa_name = []
	for root, dirs, files in os.walk(dir):
		for file in files:
			fa_name.append(os.path.join(root, file))
	
	return fa_name
	
	
def parse_fa(f):
	seqs = {}
	num_seqs = 0
	for line in f:
		if line.startswith(">"):
			num_seqs += 1
			seq_name = line.strip()[1:]
			seqs[seq_name] = str()
		else:
			seqs[seq_name] += line.strip()
	return seqs, num_seqs
	
	
def parse_depth(f):
	scaffold_depth = {}
	depth_header = f.readline().strip().split("\t")[1:]
	# contigName	contigLen	totalAvgDepth	scaffolds_h0.bbmap.sorted.bam	scaffolds_h0.bbmap.sorted.bam-var       
	for line in f:
		list = line.strip().split("\t")
		scaffold_depth[list[0]] = "\t".join(list[1:])
	return depth_header, scaffold_depth
	

def parse_blast_rdp(f):
	scaffold_taxon = {}
	for line in f:
		list = line.strip().split("\t")
		# retrieve alignLenth and taxon info
		scaffold_taxon[list[0]] = "\t".join([list[3],list[-1]])
	return scaffold_taxon
	
	
def parse_kaiju(f):
	scaffold_kaiju = {}
	for line in f:
		list = line.strip().split("\t")
		# retrieve kaiju classified result
		scaffold_kaiju[list[1]] = list[-1]
	return scaffold_kaiju
	
	
def parse_scaffold_scg(f):
	scaffold_scg = {}
	for line in f:
		list = line.strip().split("\t")
		scaffold_scg[list[0]] = "\t".join(list[3:])
	return scaffold_scg

def count_gc(seq):
	g_num = seq.lower().count("g")
	c_num = seq.lower().count("c")
	gc_perc = (g_num + c_num) /len(seq)
	return gc_perc



def main(args):
	out_title = ["Scaffold id","Genome id", "# scaffolds", "Scaffold length (bp)", "Scaffold GC"]
	
	if args.isscg:
		f_sscg = open(args.isscg, "r")
		scaffold_scg = parse_scaffold_scg(f_sscg)
		f_sscg.close()
		out_title.extend(["scg", "scg_num", "overcopy", "overcopy_num"])
		
	if args.idepth:
		f_depth = open(args.idepth, "r")
		depth_header, scaffold_depth = parse_depth(f_depth)
		f_depth.close()
		out_title.extend(depth_header)
	
	if args.irdp:
		f_rdp = open(args.irdp, "r")
		scaffold_taxon = parse_blast_rdp(f_rdp)
		f_rdp.close()
		out_title.append("alignLenth\trdp_taxon")
	
	if args.ikaiju:
		f_kaiju = open(args.ikaiju, "r")
		scaffold_kaiju = parse_kaiju(f_kaiju)
		f_kaiju.close()
		out_title.append("kaiju_taxon")
		
	out = open(args.o, "w")
	out.writelines(["\t".join(out_title), "\n"])
	
	fa_paths = get_fa_path(args.ibindir)
	for fa in fa_paths:
		f_fa = open(fa, "r")
		bin_name = ".".join(os.path.basename(fa).split(".")[0:-1])
		scaffold_seqs, num_scaffolds = parse_fa(f_fa)
		f_fa.close()
		
		for name in scaffold_seqs:
			gc = str(count_gc(scaffold_seqs[name]))
			lenth = str(len(scaffold_seqs[name]))
			out_line = [name, bin_name, str(num_scaffolds), lenth, gc]
			
			if args.isscg:
				out_line.append(scaffold_scg.get(name, "NA\tNA\tNA\tNA"))
			
			if args.idepth:
				out_line.append(scaffold_depth[name])
			
			if args.irdp:
				out_line.append(scaffold_taxon.get(name, "NA\tNA"))
			
			if args.ikaiju:
				out_line.append(scaffold_kaiju.get(name, "NA"))
			
			out.writelines(["\t".join(out_line), "\n"])
	out.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "generate total info table for every bin")
	parser.add_argument("-ibindir", type=str, help = "<dir> name of dir which contain bin fasta")
	parser.add_argument("-idepth", type=str, help = "<table> name of depth file which was created by metabat")
	parser.add_argument("-irdp", type=str,help="<table> name of file which contain the result of scaffold blast rdp database (the last coloum must be lineage info)")
	parser.add_argument("-ikaiju", type=str, help="<table> name of file which contain kaiju result (the last coloum must be lineage info)")
	parser.add_argument("-isscg", type=str, help="<table > name of file which contain scaffold to scg info")
	parser.add_argument("-o", type=str, default="total_info_for_bin.txt",help="<otu> name of output file")
	
	args = parser.parse_args()
	
	main(args)