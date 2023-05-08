import matplotlib.pyplot as plt

D = {u'Method 1':0.00418, u'Method 2': 0.0105, u'Method 3':0.0005}

plt.bar(range(len(D)), list(D.values()), align='center')
plt.xticks(range(len(D)), list(D.keys()))
plt.xlabel('Method Type')
plt.ylabel('Average Increase in Total Wireage')

plt.savefig("wire_length_change.png")
plt.clf()


import pandas as pd

change = [0.1284, 0.3271, 0.019]
variance = [0.0584, 0.139, 0.006]
index = ['Method 1', 'Method 2', 'Method 3',]
df = pd.DataFrame({'Negative Change': change,
                    'Variance': variance}, index=index)
ax = df.plot.bar(rot=0, color={"Negative Change": "green", "Variance": "orange"})
plt.xlabel('Method Type')
plt.ylabel('% decrease in capacity of overworked substation')


plt.savefig('bar_plot_with_error_bars.png')
plt.clf()

xpoints = [0.02, 0.05, 0.1, 0.3, 0.5]
change = [0.176, 0.379, 0.492, 0.761, 0.816]
plt.plot(xpoints, change)
plt.xlabel('Constant Value')
plt.ylabel('% decrease in capacity of overworked substation')
plt.savefig('change.png')
plt.clf()
