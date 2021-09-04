import argparse
import isoform

if __name__ == '__main__':

	## Command Line Interface ##

	parser = argparse.ArgumentParser(
		description='Alternative Splice Generator')
	parser.add_argument('fasta', type=str, metavar='<file>',
		help='input fasta file (reads only the first sequence if multi-fasta)')
	parser.add_argument('--min_intron', required=False, type=int, default=35,
		metavar='<int>', help='minimum length of intron [%(default)i]')
	parser.add_argument('--min_exon', required=False, type=int, default=25,
		metavar='<int>', help='minimum length exon [%(default)i]')
	parser.add_argument('--max_splice', required=False, type=int, default=3,
		metavar='<int>', help='maximum number of introns [%(default)i]')
	parser.add_argument('--flank', required=False, type=int, default=99,
		metavar='<int>', help='genomic flank on each side [%(default)i]')
	parser.add_argument('--dpwm', required=False, type=str, metavar='<file>',
		help='position weight matrix for donor site [%(default)s]')
	parser.add_argument('--apwm', required=False, type=str, metavar='<file>',
		help='position weight matrix for acceptor site [%(default)s]')
	parser.add_argument('--emm', required=False, type=str, metavar='<file>',
		help='markov model for exon sequence [%(default)s]')
	parser.add_argument('--imm', required=False, type=str, metavar='<file>',
		help='markov model for intron sequence [%(default)s]')
	parser.add_argument('--elen', required=False, type=str, metavar='<file>',
		help='length model for exons [%(default)s]')
	parser.add_argument('--ilen', required=False, type=str, metavar='<file>',
		help='length model for introns [%(default)s]')
	parser.add_argument('--introns', required=False, type=str, metavar='<file>',
		help='use introns in gff for source of splice sites [%(default)s]')
	parser.add_argument('--limit', required=False, type=int, default=20,
		metavar='<int>', help='limit number of transcripts [%(default)i]')
	"""
	parser.add_argument('--wdpwm', required=False, type=float, default=1.0,
		metavar='<float>', help='dpwm weight [%(default).2f]')
	parser.add_argument('--wapwm', required=False, type=float, default=1.0,
		metavar='<float>', help='apwm weight [%(default).2f]')
	parser.add_argument('--wemm', required=False, type=float, default=1.0,
		metavar='<float>', help='emm weight [%(default).2f]')
	parser.add_argument('--wimm', required=False, type=float, default=1.0,
		metavar='<float>', help='imm weight [%(default).2f]')
	parser.add_argument('--welen', required=False, type=float, default=1.0,
		metavar='<float>', help='elen weight [%(default).2f]')
	parser.add_argument('--wilen', required=False, type=float, default=1.0,
		metavar='<float>', help='ilen weight [%(default).2f]')

	is there a state-switching (splicing) cost?
	why do 3 splice introns score better than the real 2 in 777?
	what combinations of weights best match real data?
	"""
	arg = parser.parse_args()

	dpwm = isoform.read_pwm(arg.dpwm)   if arg.dpwm else None
	apwm = isoform.read_pwm(arg.apwm)   if arg.apwm else None
	elen = isoform.read_len(arg.elen)   if arg.elen else None
	ilen = isoform.read_len(arg.ilen)   if arg.ilen else None
	emm  = isoform.read_markov(arg.emm) if arg.emm  else None
	imm  = isoform.read_markov(arg.imm) if arg.imm  else None

	name, seq = next(isoform.read_fasta(arg.fasta))
	txs, info = isoform.all_possible(seq, arg.min_intron, arg.min_exon,
		arg.max_splice, arg.flank, gff=arg.introns)

	for tx in txs:
		score = 0
		if apwm: score += isoform.score_apwm(apwm, tx)
		if dpwm: score += isoform.score_dpwm(dpwm, tx)
		if elen: score += isoform.score_elen(elen, tx)
		if ilen: score += isoform.score_ilen(ilen, tx)
		if emm:  score += isoform.score_emm(emm, tx)
		if imm:  score += isoform.score_imm(imm, tx, dpwm, apwm)
		tx['score'] = score

	print('# seq:', name)
	print('# len:', len(seq))
	print('# donors:', info['donors'])
	print('# acceptors:', info['acceptors'])
	print('# trials:', info['trials'])
	print('# isoforms:', len(txs))
	print('# entropy:', isoform.complexity(txs))

	limit = arg.limit if arg.limit else len(txs)
	txs = sorted(txs, key=lambda item: item['score'], reverse=True)

	# calculate probability of each isoform
	weight = []
	total = 0
	for tx in txs:
		w = 2 ** tx['score']
		weight.append(w)
		total += w
	prob = []
	for w in weight: prob.append(w / total)

	# create gff
	chrom = name.split()[0]
	src = 'asg'
	cs = f'{chrom}\t{src}\t'
	b = txs[0]['beg'] + 1
	e = txs[0]['end'] + 1
	gene = f'Gene-{chrom}'
	print(f'{cs}gene\t{b}\t{e}\t.\t+\t.\tID={gene}\n') # gene
	for i in range(limit):
		tx = txs[i]
		b = tx['beg'] + 1
		e = tx['end'] + 1
		s = prob[i]
		tid = f'tx-{chrom}-{i+1}'
		print(f'{cs}mRNA\t{b}\t{e}\t{s:.4g}\t+\t.\tID={tid};Parent={gene}') # tx
		for exon in tx['exons']:
			b = exon[0] + 1
			e = exon[1] + 1
			print(f'{cs}exon\t{b}\t{e}\t.\t+\t.\tParent={tid}') # exons
		print()
