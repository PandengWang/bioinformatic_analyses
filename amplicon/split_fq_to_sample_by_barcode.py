#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'Pandeng Wang'
__version__ = '1.0'
__date__ = '2017-08-02'

import sys
import argparse
import os

def correct_barcode(query_seq, seq_possibilities):
	""" finds closest (by nt seq edit distance) match to query_seq

	assumes:
	all sequences are same length
	no sequence appears twice in seq_possibilities

	returns (best_hit, min_dist)
	* best_hit is closest sequence from seq_possibilities, or None if a tie
	* min_dist is the edit distance between the query_seq and the best hit
	cw1 = AAACCCGGGTTT (12 nucleotides)
	cw2 = AAACCCGGGTTA (edit distance of 1 from cw1)
	cw3 = AAACCCGGGTTG (edit distance of 1 from cw1)
	cw4 = AAACCCGGGTTC (edit distance of 1 from cw1)
	cw5 = AAACCCGGGTGG (edit distance of 2 from cw1)
	"""
	dists = [_edit_dist(query_seq, seq) for seq in seq_possibilities]
	min_dist = min(dists)
	number_mins = dists.count(min_dist)
	if number_mins > 1:
		return None, min_dist
	else:
		best_hit = seq_possibilities[dists.index(min_dist)]
		return best_hit, min_dist


def _edit_dist(s1, s2):
    """ computes edit (hamming) between to strings of equal len

    designed for strings of nucleotides, not bits"""
    dist = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            dist += 1
    return dist


def parse_fq(f, r):
	while 1:
		if f.readline() and r.readline():
			fseq = f.readline().strip()
			rseq = r.readline().strip()
			f.readline()
			r.readline()
			fqua = f.readline().strip()
			rqua = r.readline().strip()
			yield fseq, fqua, rseq, rqua
		else:
			break


def parse_barcode(f):
	bc_to_sid = {}
	for line in f:
		line = line.strip()
		list = line.split()
		bc_to_sid[list[0]] = list[1]
	return bc_to_sid


def parse_oligos(f):
	bc_to_sid = {}
	for line in f:
		if line.startswith("barcode"):
			list = line.split()
			bc_to_sid[list[1]] = list[2]
		else:
			pass
	return bc_to_sid


def main(argv):

	bdiffs = argv.bdiffs
	blen = argv.blen
	llen = argv.llen
	outdir = argv.odir
	if os.path.exists(outdir):
		pass
	elif os.path.isdir(outdir):
		pass
	else:
		os.mkdir(outdir)
	
	sid_seqs = {}
	sid_seqs_num = {}
	
	try:
		ifq1 = open(argv.ifq1, "r")
	except:
		raise IOError
	try:
		ifq2 = open(argv.ifq2, "r")
	except:
		raise IOError
	
	if argv.bc:
		try:
			ibc = open(argv.bc, "r")
		except:
			raise IOError
		bc_to_sid = parse_barcode(ibc)
	elif argv.oligos:
		try:
			ibc = open(argv.oligos, "r")
		except:
			raise IOError
		bc_to_sid = parse_oligos(ibc)
	else:
		raise IOError("no barcode or oligos file")
		
	barcodes = bc_to_sid.keys()
	for sample in bc_to_sid.values():
		sid_seqs[sample] = []
		sid_seqs_num[sample] = 0
	# print(sid_seqs.values())
	for fseq, fqual, rseq, rqual in parse_fq(ifq1, ifq2):
		
		if bdiffs == 0:
			for bc in barcodes:
				if bc in fseq[:(blen+10)]:
					sid_seqs[bc_to_sid[bc]].append((fseq[blen+llen:], fqual[blen+llen:], rseq, rqual))
					sid_seqs_num[bc_to_sid[bc]] = sid_seqs_num[bc_to_sid[bc]] + 1
				elif bc in rseq[:20]:
					sid_seqs[bc_to_sid[bc]].append((rseq[blen+llen:], rqual[blen+llen:], fseq, fqual))
					sid_seqs_num[bc_to_sid[bc]] = sid_seqs_num[bc_to_sid[bc]] + 1
				else:
					pass
		else:
			
			fposi_barcode = fseq[:blen]
			rposi_barcode = rseq[:blen]
			(fbest_hit, fmin_dist) = correct_barcode(fposi_barcode, barcodes)
			(rbest_hit, rmin_dist) = correct_barcode(rposi_barcode, barcodes)
			if not fbest_hit and not rbest_hit:
				pass
			elif fmin_dist < rmin_dist:
				if fmin_dist <= bdiffs and fbest_hit:
					sid_seqs[bc_to_sid[fbest_hit]].append((fseq[blen+llen:], fqual[blen+llen:], rseq, rqual))
					sid_seqs_num[bc_to_sid[fbest_hit]] = sid_seqs_num[bc_to_sid[fbest_hit]] + 1
				else:
					pass
			elif fmin_dist > rmin_dist:
				if rmin_dist <= bdiffs and rbest_hit:
					sid_seqs[bc_to_sid[rbest_hit]].append((rseq[blen+llen:], rqual[blen+llen:], fseq, fqual))
					sid_seqs_num[bc_to_sid[rbest_hit]] = sid_seqs_num[bc_to_sid[rbest_hit]] + 1
				else:
					pass
			else:
				pass


	for key in sid_seqs.keys():
		foutf = os.path.join(outdir, key + "_R1.fq")
		routf = os.path.join(outdir, key + "_R2.fq")
		fout = open(foutf, "w")
		rout = open(routf, "w")
		i = 1
		for fseq, fqual, rseq, rqual in sid_seqs[key]:
			fout.writelines(["@"+key+"_"+str(i)+"\n", fseq+"\n", "+\n", fqual+"\n"])
			rout.writelines(["@"+key+"_"+str(i)+"\n", rseq+"\n", "+\n", rqual+"\n"])
			i += 1
		fout.close()
		rout.close()
		print("%s	%d"%(key, sid_seqs_num[key]))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Split library by barcode.")
	parser.add_argument("-ifq1", type=str, help="Input: R1 file (fastq)", required=True)
	parser.add_argument("-ifq2", type=str, help="Input: R2 file (fastq)", required=True)
	parser.add_argument("-bc", type=str, help="Input: barcodes file (tab table)")
	parser.add_argument("-oligos", type=str, help="Input: oligos file, you should provide one barcodes file or oligos file, don't need both (tab table)")
	parser.add_argument("-odir", type=str, help="Output: output directory", required=True)
	parser.add_argument("-bdiffs", type=int, default=0, help="Max num of barcode mismatch to be allowed (default:0)")
	parser.add_argument("-blen", type=int, default=12, help="Barcodes length (default:12)")
	parser.add_argument("-llen", type=int, default=2, help="Linker nt length (default:2)")
	args = parser.parse_args()
	main(args)
