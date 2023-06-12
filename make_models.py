import argparse
import gzip
import modelib as ml
import csv

parser = argparse.ArgumentParser(
	description='Generates len, MM, and PWM models for apc')

parser.add_argument('--extxt', type=str, metavar='<file>', 
	required=False, help='input text file with exon sequences')
parser.add_argument('--intxt', type=str, metavar='<file>',
	help='input text file with intron sequences')
parser.add_argument('--dntxt', type=str, metavar='<file>',
	help='input text file with donor site sequences')
parser.add_argument('--actxt', type=str, metavar='<file>',
	help='input text file with acceptor site sequences')
parser.add_argument('-mm', action='store_true')
parser.add_argument('-len', action='store_true')
#parser.add_argument('-pwm', action='store_true')

args = parser.parse_args()

fp = args.actxt
print(fp)

'''
# note: parameters/best fit dist change depending on maximum length considered
# exon lens cutoff at 250 have a weibull distribution
# exon lens cutoff at 500/1000 have a frechet distribution
# if no cutoff, both are frechet
# leave default in ml.memoize_fdist to 1000 so both have a frechet distribution
def len_tsv_write(exins, fp):
	
	exinlen_yscores, exinlen_yvalues = ml.memoize_fdist(exins, pre2=6)

	root, ext = fp.split('.')
	filename = root + '_len' + '.tsv'

	with open(filename, 'w', newline='') as tsvfile:
		writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
		writer.writerow([root+' len %', root+' len log2(%)'])
		for i in range(len(exinlen_yscores)):
			writer.writerow([exinlen_yvalues[i], exinlen_yscores[i]])
	tsvfile.close()

def mm_tsv_write(exins, fp):

	exinmm_scores, exinmm_probs = ml.make_mm(exins)

	root, ext = fp.split('.')
	filename = root + '_mm' + '.tsv'

	with open(filename, 'w', newline='') as tsvfile:
		writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
		writer.writerow([root+' mm kmer', root+' mm %', root+' mm log2(%)'])
		for key in exinmm_scores:
			writer.writerow([key + 'A', exinmm_probs[key][0], 
				exinmm_scores[key][0]])
			writer.writerow([key + 'C', exinmm_probs[key][1], 
				exinmm_scores[key][1]])
			writer.writerow([key + 'G', exinmm_probs[key][2], 
				exinmm_scores[key][2]])
			writer.writerow([key + 'T', exinmm_probs[key][3], 
				exinmm_scores[key][3]])
	tsvfile.close()

if args.extxt and args.mm:
	exons = ml.read_txt_seqs(args.extxt)
	mm_tsv_write(exons, args.extxt)
elif args.extxt and args.len:
	len_tsv_write(exons, args.extxt)
	exons = ml.read_txt_seqs(args.extxt)	
elif args.extxt:
	exons = ml.read_txt_seqs(args.extxt)
	len_tsv_write(exons, args.extxt)
	mm_tsv_write(exons, args.extxt)
							
if args.intxt and args.mm:
	introns = ml.read_txt_seqs(args.intxt)
	mm_tsv_write(introns, args.intxt)
elif args.intxt and args.len:
	introns = ml.read_txt_seqs(args.intxt)
	len_tsv_write(introns, args.intxt)
elif args.intxt:
	introns = ml.read_txt_seqs(args.intxt)
	len_tsv_write(introns, args.intxt)
	mm_tsv_write(introns, args.intxt)

####################################################

def pdread(dictionary):

	for site in dictionary:
		A = None
		C = None
		G = None
		T = None
		for key in site:
			if key == 'A':
				A = site[key]
			if key == 'C':
				C = site[key]
			if key == 'G':
				G = site[key]
			if key == 'T':
				T = site[key]
		yield [A, C, G, T]

def de(num, pre=6):
	
	num2 = f'{num:.{pre}f}'
	return num2

def pwm_tsv_write(donacc, fp):

	pwm, ppm = ml.make_pwm(donacc)

	fp = args.dntxt
	root, ext = fp.split('.')
	filename = root + '_pwm' + '.tsv'

	with open(filename, 'w', newline='') as tsvfile:
		writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
		writer.writerow([root+' % ppm'])
		for site in pdread(ppm):
			a = de(site[0])
			c = de(site[1])
			g = de(site[2])
			t = de(site[3])
			writer.writerow([a, c, g, t])
		writer.writerow([root+' log2(%) pwm'])
		for site in pdread(pwm):
			a = de(site[0])
			c = de(site[1])
			g = de(site[2])
			t = de(site[3])	
			writer.writerow([a, c, g, t])
	tsvfile.close()

if args.dntxt:
	donors = ml.read_txt_seqs(args.dntxt)
	pwm_tsv_write(donors, args.dntxt)

if args.actxt:
	acceptors = ml.read_txt_seqs(args.actxt)
	pwm_tsv_write(acceptors, args.actxt)
'''






