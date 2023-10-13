import argparse
import os

parser = argparse.ArgumentParser(description=
	'writes file with command line arguments to be used in parallize')
parser.add_argument('apc_dir', type=str, metavar='<str>', 
	help='directory with apc fasta and gff files')
parser.add_argument('--read_gff', action='store_true', 
	help='get don/acc sites from gff files in apc dir')

# apc parameters
parser.add_argument('--max_splice', required=False, type=int, default=3,
	metavar='<int>', help='maximum number of splicing events %(default)d')
parser.add_argument('--min_intron', required=False, type=int, default=25,
	metavar='<int>', help='minimum length of intron %(default)d')
parser.add_argument('--min_exon', required=False, type=int, default=25,
	metavar='<int>', help='minimum length of exon %(default)d')
parser.add_argument('--flank', required=False, type=int, default=100,
	metavar='<int>', help='length of genomic flank on each side %(default)d')
parser.add_argument('--limit', required=False, type=int, default=20, 
	metavar='<int>', help='limit number of saved apc isoforms %(default)d')

# probabilistic models
parser.add_argument('--exon_len', required=False, type=str, metavar='<file>', 
	help='exon length model .tsv')
parser.add_argument('--intron_len', required=False, type=str, metavar='<file>',
	help='intron length model .tsv')
parser.add_argument('--exon_mm', required=False, type=str, metavar='<file>',
	help='exon markov model .tsv')
parser.add_argument('--intron_mm', required=False, type=str, metavar='<file>',
	help='intron markov model .tsv')
parser.add_argument('--donor_pwm', required=False, type=str, metavar='<file>',
	help='donor pwm .tsv')
parser.add_argument('--acceptor_pwm', required=False, type=str, metavar='<file>',
	help='acceptor pwm .tsv')
parser.add_argument('--icost', required=False, type=float, default=0.0,
	metavar='<float>', help='intron cost %(default).2d')
	
args = parser.parse_args()

fa_gff_pairs = {}
for fname in os.listdir(args.apc_dir):
	ID = fname.split('.')[1]
	if ID not in fa_gff_pairs:
		fa_gff_pairs[ID] = [args.apc_dir + fname]
	else:
		fa_gff_pairs[ID] += [args.apc_dir + fname]


	

print(fa_gff_pairs)	
gene_path = 'wow'
f = open('apc_cmds.txt', 'w')
flag = ''
if args.read_gff:
	flag = ' --read_gff'
f.write(
	f'python3 apc_isogen.py {gene_path}'
	f'{flag}'
	f' --min_intron {args.min_intron} --min_exon {args.min_exon}'
	f' --flank {args.flank} --limit {args.limit}'
	f' --exon_len {args.exon_len} --intron_len {args.intron_len}'
	f' --exon_mm {args.exon_mm} --intron_mm {args.intron_mm}'
	f' --donor_pwm {args.donor_pwm} --acceptor_pwm {args.acceptor_pwm}
)
#f.write(f'new line with stuff')
f.close()






