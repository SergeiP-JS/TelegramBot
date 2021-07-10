#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'SPridannikov'


import math
import os


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import ticker

# data = {'series1':[1,3,4,3,5],
#         'series2':[2,4,5,2,4],
#         'series3':[3,2,3,1,3]}


def create_graph(days,items):
        # print(days,items)
        data = {'USD':items}
        df = pd.DataFrame(data)
        x = np.arange(start=1, stop=days+1)

        plt.axis([1,days+1,int(math.floor(min(items))),int(math.ceil(max(items)))])
        plt.plot(x,df)
        # plt.legend(data, loc=1)
        # plt.show()
        if not os.path.isdir('img'):
                os.mkdir('img')

        if os.path.isfile(f'img/graph_{days}.png'):
                os.remove(f'img/graph_{days}.png')
                plt.savefig(f'img/graph_{days}.png',transparent=True,bbox_inches='tight')
        else:
                plt.savefig(f'img/graph_{days}.png', transparent=True, bbox_inches='tight')


# create_graph(3,[2,4,5])