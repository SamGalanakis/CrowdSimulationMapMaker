import seaborn as sns
import matplotlib.pyplot as plt

import numpy as np
from os import listdir
from os.path import isfile, join

sns.set_style("darkgrid")





time=np.linspace(0,5*60,5*60*4)


fig, ax = plt.subplots()
ax.set_xlabel("Time (s)")
ax.set_ylabel(" Average speed (m/s)")
# ax.set_title("Social distancing with patience")

sns.set_palette("Reds")
with open("patience_avg_velocity.txt") as fp:
    data=[float(line) for line in fp]
    data=data[0:len(time)]

    ax.plot(time,data)

with open("no_patience_avg_velocity.txt") as fp:
    data=[float(line) for line in fp]
    data=data[0:len(time)]
   
    ax.plot(time,data)


with open("default_avg_velocity.txt") as fp:
    data=[float(line) for line in fp]
    data=data[0:len(time)]

    ax.plot(time,data)

ax.legend(labels=["With Patience","Without Patience","No distancing"])
plt.show()











