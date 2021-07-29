# rewrite/methods check of code using combinations()
# need to integrate the following parameters:
# seq, minin, minex, dons, accs
# output should be the same as isoform.py/isoformer.py

import itertools as it

# all sites need to be sorted
don_sites=[2,9,14,24,25]
acc_sites=[11,20,26]

def makesnosense(dons,accs):
	for d,a in zip(dons,accs):
		if d>a: return True
	return False
	
def short_introns(dons,accs,minintron):
	for d,a in zip(dons,accs):
		intron_length=a-d
		if intron_length<minintron:
			return True
	return False
	
def short_exons(dons,accs,minexon):
	for i in range(1,len(dons)):
		exon_begin=accs[i-1]+1
		exon_end=dons[i]-1
		exon_length=exon_end-exon_begin
		if exon_length<minexon: 
			return True
	return False

trials=0
coor_fails=0
intron_fails=0
exon_fails=0
for n in range(1,len(don_sites)+1):
	for d in it.combinations(don_sites,n):
		for a in it.combinations(acc_sites,n):
			trials+=1
			if makesnosense(d,a): 
				coor_fails+=1
				continue	
			if short_introns(d,a,4):
				intron_fails+=1
				continue	
			if short_exons(d,a,1):
				exon_fails+=1
				continue				
			print(d,a)
				
print('trials:',trials,'coor_fails:',coor_fails,'intron_fails:',intron_fails,'exon_fails:',exon_fails)	

# next: generate random sequences of various lengths
# plot the number of trials 
# look at scalability
# use multiple 100 bp sequnces, multiple 200 bp sequences, etc. 
# then do this for actual sequences
					
				
				
				

