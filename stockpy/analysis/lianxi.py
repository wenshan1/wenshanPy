#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 16:02:17 2018

@author: wenshan
"""


# sphinx_gallery_thumbnail_number = 3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

a = pd.DataFrame(np.random.rand(4,5), columns = list('abcde'))
a_asndarray = a.values

x = np.linspace(0, 2, 100)

plt.plot(x, x, label='linear')
plt.plot(x, x**2, label='quadratic')
plt.plot(x, x**3, label='cubic')

plt.xlabel('x label')
plt.ylabel('y label')

plt.title("Simple Plot")

plt.legend()

plt.show()


x = np.arange(0, 10, 0.2)
y = np.sin(x)
fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()