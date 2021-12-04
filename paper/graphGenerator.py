#!/usr/bin/env python3

import matplotlib.pyplot as plt

n = 2002
labels = ['Approves', "Disapproves", "Doesn't know/didn't answer"]
vals = [601, 1321, 80]
err = [x*0.01*n for x in [2, 2, 2]]

fig, ax = plt.subplots()

bars = ax.bar(labels, vals, yerr=err, label="Percentage of \ntotal responses")
for bar in bars:
    height = bar.get_height()
    ax.text(x=bar.get_x() + bar.get_width()/4, y=height+(0.02*max(vals)),
            s="{:.1f}%".format(round((height/n)*100)),
      ha='center')

ax.set_ylabel('Number of responses')
ax.set_title('Number of answers per category')
ax.legend()

plt.savefig("ValsIPEC.png")
