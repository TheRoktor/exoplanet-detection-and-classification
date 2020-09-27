import pandas as pd
import time
import sklearn as skl
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sn
import sys
plt.style.use('seaborn-whitegrid')

# features used
#49 = kepler name
#47 = pdisposition
#46 = disposition
#43 = score

start = time.time()

original_stdout = sys.stdout # Save a reference to the original standard output

f = open('report.txt', 'w+')
sys.stdout = f 



kepler = pd.read_csv('keplerfull2.csv')
kepler = kepler.drop(kepler.columns[0], axis=1)


keys = ['total','confirmed', 'candidate', 'false', 'named']
keys2 = ['number', 'totalScore']
dispositionDict = dict.fromkeys(keys)
pdispositionDict = dict.fromkeys(['candidate', 'false'])

candidateToConfirmed = 0
candidateToFalse = 0
candidateToCandidate = 0

falseToConfirmed = 0
falseToFalse = 0



for key in dispositionDict.keys():
    dispositionDict[key] = dispositionDict.fromkeys(keys2)
    for key2 in dispositionDict[key].keys():
        dispositionDict[key][key2] = 0

for key in pdispositionDict.keys():
    pdispositionDict[key] = pdispositionDict.fromkeys(keys2)
    for key2 in pdispositionDict[key].keys():
        pdispositionDict[key][key2] = 0



correctPredispositions = 0
for row in kepler.itertuples(index=True):
    dispositionDict['total']['totalScore'] += row[42]
    dispositionDict['total']['number'] += 1


    if str(row[46]) == str(row[45]):
        correctPredispositions += 1

    if(str(row[46]) == 'CANDIDATE'):
        pdispositionDict['candidate']['number'] += 1
        pdispositionDict['candidate']['totalScore'] += row[42]
        if(str(row[45]) == 'CONFIRMED'):
            candidateToConfirmed += 1
            dispositionDict['confirmed']['number'] += 1
            dispositionDict['confirmed']['totalScore'] += row[42]
            if (str(row[48]) != 'nan'):
                dispositionDict['named']['totalScore'] += row[42]
                dispositionDict['named']['number'] += 1

        elif str(row[45]) == 'FALSE POSITIVE':
            print("sem tu")
            dispositionDict['false']['totalScore'] += row[42]
            dispositionDict['false']['number'] += 1
            candidateToFalse += 1

        elif str(row[45]) == 'CANDIDATE':
            candidateToCandidate += 1
            dispositionDict['candidate']['totalScore'] += row[42]
            dispositionDict['candidate']['number'] += 1

    else:

        pdispositionDict['false']['number'] += 1
        pdispositionDict['false']['totalScore'] += row[42]
        if (str(row[45]) == 'CONFIRMED'):
            falseToConfirmed += 1
            dispositionDict['confirmed']['totalScore'] += row[42]
            dispositionDict['confirmed']['number'] += 1

        elif str(row[45]) == 'FALSE POSITIVE':
            falseToFalse += 1
            dispositionDict['false']['totalScore'] += row[42]
            dispositionDict['false']['number'] += 1



for key in dispositionDict:
    print(key + " total number of planets: " + str(dispositionDict[key]['number']))
    print(key + " avreage score: " + str(dispositionDict[key]['totalScore'] / dispositionDict[key]['number'])+"\n")


print("# of candidates to confirmed: "+str(candidateToConfirmed))
print("% of candidates to confirmed " + str(candidateToConfirmed / pdispositionDict['candidate']['number']) + "\n")


print("# of candidates to false: " + str(candidateToFalse))
print("% of candidates to false: " + str(candidateToFalse / pdispositionDict['candidate']['number']) + "\n")

print("# of false to false: "+str(falseToFalse))
print("% of false to false: " + str(falseToFalse / pdispositionDict['false']['number']) + "\n")

print("# of false to confirmed: "+str(falseToConfirmed))
print("% of false to confirmed: " + str(falseToConfirmed / dispositionDict['false']['number']) + "\n")


print("# of correct predispositions: "+str(correctPredispositions))
print("% of correct predispositions: " + str(correctPredispositions / dispositionDict['total']['number']) + "\n")

endAvreages = time.time()
print("Time of execution of avreage and percentage computations: "+str(endAvreages-start))
startPlots = time.time()

labels = 'Confirmed', 'False positive', 'Candidate' #how many candidate planets went from the 'CANDIDATE' category to the others
sizes = [candidateToConfirmed/pdispositionDict['candidate']['number'], candidateToFalse/pdispositionDict['candidate']['number'], 1 - (candidateToFalse/pdispositionDict['candidate']['number']) - (candidateToConfirmed/pdispositionDict['candidate']['number'])]
explode = (0.05, 0.05, 0.05)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.legend(labels, loc='best', bbox_to_anchor=(-0.1, 1.),
           fontsize=8)
plt.show()
fig1.savefig('candidateToOthers.png')


labels2 = 'Confirmed', 'False positive'
sizes2 = [falseToConfirmed/pdispositionDict['false']['number'], falseToFalse/pdispositionDict['false']['number']]
explode2 = (0, 0.4)

fig2, ax2 = plt.subplots()
ax2.pie(sizes2, explode=explode2, autopct='%1.1f%%',
        shadow=True, startangle=9045)
ax2.axis('equal')  
plt.legend(labels, loc='best', bbox_to_anchor=(-0.1, 1.),
           fontsize=8)
plt.show()
fig2.savefig('falseToOthers.png')


x = np.linspace(0,dispositionDict['total']['number'],num=dispositionDict['total']['number'])
scores = kepler['score']


a = scores.sort_values().tolist()

plt.axis([0,9564,0,1])
plt.plot(x, a, 'o', markersize=0.1, color='black')
plt.savefig('graph1.png', dpi=900)
plt.show()

corr = kepler.corr()


sn.heatmap(corr, annot=True)
plt.figure(figsize=(16,9))
ax = sn.heatmap(
    corr,
    vmin=-1, vmax=1, center=0,
    cmap=sn.diverging_palette(20, 220, n=200),
    square=True
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=90,
    horizontalalignment='right'
);
plt.show()
ax.figure.savefig('corrs.png')

endPlots = time.time()


print("Time of execution of plotting: "+str(endPlots-startPlots))
print("Total time of execution: "+str(endPlots-start))

sys.stdout = original_stdout 