#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'Pandeng Wang'
__version__ = '1.0'
__date__ = '2018-01-12'

import sys
import os
import argparse
import json


def parse_bin_stats_ext(f):
	bin_to_scgInfo = {}
	for line in f:
		list = line.strip().split("\t")
		bin_to_scgInfo[list[0]] = list[1]
	return bin_to_scgInfo 
	
	
def parse_marker_gene_stats(f):
	bin_to_scaffoldInfo = {}
	for line in f:
		list = line.strip().split("\t")
		bin_to_scaffoldInfo[list[0]] = list[1]
	return bin_to_scaffoldInfo


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "parse checkM 'bin_stats_ext.tsv' and 'marker_gene_stats.tsv'")
	parser.add_argument("-ib", type=str, help = "<table> input 'bin_stats_ext.tsv' file")
	parser.add_argument("-im", type=str, help = "<table> input 'marker_gene_stats.tsv' file")
	parser.add_argument("-oscg", type=str, default="bin_to_single_copy_gene_info.txt",help="<out> output bin to SCG info file")
	parser.add_argument("-osaf", type=str, default="scaffold_to_single_copy_gene_info.txt", help="<out> output scaffold to SCG info file")
	
	args = parser.parse_args()
	
	ib = open(args.ib, "r")
	bin_to_scgInfo = parse_bin_stats_ext(ib)
	ib.close()
	
	im = open(args.im, "r")
	bin_to_scaffoldInfo = parse_marker_gene_stats(im)
	im.close()
	
	out1 = open(args.oscg, "w")
	out2 = open(args.osaf, "w")
	
	for bin in bin_to_scgInfo:
		dic1 = json.loads(bin_to_scgInfo[bin].replace("\'", "\""))
		dic2 = json.loads(bin_to_scaffoldInfo[bin].replace("\'", "\""))
		
		num_scaffolds = dic1["# scaffolds"]
		scg_dic = {}
		over_copy_gene = []
		if dic1["GCN0"]:
			for gene in dic1["GCN0"]:
				scg_dic[gene] = [0,]
		
		if dic1["GCN1"]:
			for gene in dic1["GCN1"]:
				scg_dic[gene] = [1,]
		
		if dic1["GCN2"]:
			for gene in dic1["GCN2"]:
				scg_dic[gene] = [2,]
				over_copy_gene.append(gene)
		
		if dic1["GCN3"]:
			for gene in dic1["GCN3"]:
				scg_dic[gene] = [3,]
				over_copy_gene.append(gene)
		
		if dic1["GCN4"]:
			for gene in dic1["GCN4"]:
				scg_dic[gene] = [4,]
				over_copy_gene.append(gene)
		
		if dic1["GCN5+"]:
			for gene in dic1["GCN5+"]:
				scg_dic[gene] = ["5+",]
				over_copy_gene.append(gene)
		
		scaffold_to_scg = {}
		## Below is the first version which has a bug that can lead to missing some intersection
		## between over_copy_gene and scg of every scaffold
		# for scaffold in dic2.keys():
			# scg = sorted(dic2[scaffold].keys())
			# scaffold_name = "_".join(scaffold.split("_")[0:-1])
			# if scaffold_name in scaffold_to_scg:
				# scaffold_to_scg[scaffold_name].extend(scg)
			# else:
				# scaffold_to_scg[scaffold_name] = scg
			
			# for s in scg:
				# s = s.split(".")[0]
				# scg_dic[s].append(scaffold_name)
		for scaffold in dic2.keys():
			scg = sorted(dic2[scaffold].keys())
			
			scg = map(lambda x: x.split(".")[0], scg)
			
			scaffold_name = "_".join(scaffold.split("_")[0:-1])
			if scaffold_name in scaffold_to_scg:
				scaffold_to_scg[scaffold_name].extend(scg)
			else:
				scaffold_to_scg[scaffold_name] = scg
			
			for s in scg:
				scg_dic[s].append(scaffold_name)
		
		for key in scg_dic.keys():
			out1.writelines([bin+"\t",key+"\t", str(scg_dic[key][0])+"\t", ";".join(scg_dic[key][1:])+"\n"])
			
		for key in scaffold_to_scg.keys():
			total_scg = scaffold_to_scg[key]
			over_copy = list(set(total_scg).intersection(set(over_copy_gene)))
			out2.writelines([key+"\t", bin+"\t", str(num_scaffolds)+"\t",";".join(total_scg)+"\t", str(len(total_scg))+"\t", ";".join(over_copy)+"\t", str(len(over_copy))+"\n"])
		
	out1.close()
	out2.close()
