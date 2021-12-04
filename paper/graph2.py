#!/usr/bin/env python3

import matplotlib.pyplot as plt

n = 1524
labels = ['Positive', "Negative", "Neutral"]
vals = [388, 836, 300]

fig, ax = plt.subplots()

bars = ax.bar(labels, vals, label="Percentage of \ntotal tweets")

for bar in bars:
    height = bar.get_height()
    ax.text(x=bar.get_x() + bar.get_width()/2, y=height+(0.01*max(vals)),
            s="{:.2f}%".format(round((height/n)*100)),
      ha='center')
ax.set_ylabel('Number of tweets')
ax.set_title('Number of tweets per category')
ax.legend()

plt.savefig("ValsTwitter.png")
