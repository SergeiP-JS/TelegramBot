import os
import time
from typing import List

import matplotlib.pyplot as plt

import db


def create_graph(items: List[db.ExchangeRate],path_graph):
    plt.clf()

    days = len(items)

    x = range(1, days + 1)
    y = [x.value for x in items]
    plt.plot(x, y)

    os.makedirs('img', exist_ok=True)
    plt.savefig(path_graph, transparent=True, bbox_inches='tight')


if __name__ == '__main__':
    items1 = db.ExchangeRate.get_last_by(days=30)
    create_graph(items1,'img/graph_s2.png')
    items2 = db.ExchangeRate.get_last_by(days=7)
    create_graph(items2, 'img/graph_s1.png')