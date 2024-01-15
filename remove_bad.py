# get old pairs in tuples (p, h, label)
lines = open('GoldenPairs-InitialVersion.tex').readlines()
i=0
old=[]
while i < len(lines):
    if lines[i][0].isdigit(): old.append((lines[i][3:].strip(), lines[i+1][3:].strip(), lines[i+1][0]))
    i+=3
print(len(old))

# get to-remove pairs in tuples (p, h, label)
lines2 = open('gold_30_ver2_gpt-4_6shots_reasonTrue_wrongs.txt').readlines()
j=0
rem = []
while j < len(lines2):
    if lines2[j].startswith('Premise: '):
        pair = (lines2[j][8:].strip(), 
                    lines2[j+1][11:].strip(),
                    lines2[j+2][7].upper())
        assert pair[2] in ['E','C','N']
        rem.append(pair)
        j += 3
    else: 
        j += 1
print(len(rem))

# sanity check
count = 0
for r in rem:
    if r not in old: 
        print(r)
        count+=1
print(count) 
# two are not there:
# ('The second application is to Hecke algebras.', 'The second application is to Hall algebras.', 'N')
# ('We combine two recent ideas: cartesian differential categories, and restriction categories.', 'We combine three ideas', 'N')
# manually corrected

# remove 
new = []
for i in old:
    if i in rem: continue
	# remove based on premise and label
    if (i[0] == 'The second application is to Hecke algebras.') and \
    	(i[2] == 'N'): continue
	# remove based on premise and label
    if (i[0] == 'We combine two recent ideas: cartesian differential categories, and restriction categories.') and \
    	(i[2] == 'N'): continue
    new.append(i)

print(len(old), len(rem), len(new))

with open('gold-final.txt','w') as f:
    for i, pair in enumerate(new):
        f.write(f'ID: {i}\nPremise: {pair[0]}\nHypothesis: {pair[1]}\nLabel: {pair[2]}\n\n')
