# lines = open('seed-final.txt').readlines()

# output = {'ID':[], 'Premise':[], 'Hypothesis':[], 'Label':[]}

# for line in lines:
#     for marker in ['ID','Premise','Hypothesis','Label']:
#         if line.startswith(marker):
#             output[marker].append(line.replace(f'{marker}:','').strip())

# assert len(output['ID']) == len(output['Premise']) == len(output['Hypothesis']) == len(output['Label'])

# with open('seed.txt', 'w') as fout:
#     for i in range(len(output['ID'])):
#         fout.write(f"{output['ID'][i]}\t{output['Premise'][i]}\t{output['Hypothesis'][i]}\t{output['Label'][i]}\n")

content = open('436_nli_0227.txt').read()
triplets = [t for t in content.split('---------------------------') if len(t) > 50]

output = {'ID':[], 'Premise':[], 'Hypothesis':[], 'Label':[]}
labels = ['entailment', 'neutral', 'contradiction']

for i, triplet in enumerate(triplets):
    lines = [l.strip() for l in triplet.strip().split('\n') if len(l.strip()) > 5]
    if lines[0][0].isdigit() and 'Sentence' in lines[0]:
        premise = lines[0].split(':')[-1].strip()
    else:
        continue
    lines_for_hypothesis = [l for l in lines[1:] if not premise in l]
    if len(lines_for_hypothesis) % 3 != 0:
        continue
    
    step = len(lines_for_hypothesis) // 3
    for j in range(0, len(lines_for_hypothesis), step):
        one_premise_fragment = '\n'.join(lines_for_hypothesis[j:j+step])
        for label in labels:
            if label in one_premise_fragment or label.capitalize() in one_premise_fragment:
                segments = sorted([l.split(':')[-1].strip() for l in one_premise_fragment.split('\n') if len(l) > 14], key=lambda x: len(x))
                try:
                    hypothesis = segments[-1]
                    output['Premise'].append(premise)
                    output['Hypothesis'].append(hypothesis)
                    output['Label'].append(label[0].upper())
                except:
                    print(segments)
                    print(i, triplet)
                    raise
            # print(label, hypothesis)
    # if i == 10: break
assert len(output['Premise']) == len(output['Hypothesis']) == len(output['Label'])

output['ID'] = [i+1 for i in range(len(output['Premise']))]
with open('gpt4-pairs.txt', 'w') as fout:
    for i in range(len(output['ID'])):
        fout.write(f"{output['ID'][i]}\t{output['Premise'][i]}\t{output['Hypothesis'][i]}\t{output['Label'][i]}\n")
