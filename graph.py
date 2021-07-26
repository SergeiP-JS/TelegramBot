import os
from typing import List

import matplotlib.pyplot as plt

import db
from config import PATH_GRAPH_WEEK,PATH_GRAPH_MONTH


def create_graph(items: List[db.ExchangeRate]):
    days = len(items)

    x = range(1, days + 1)
    y = [x.value for x in items]
    plt.plot(x, y)

    path_graph=PATH_GRAPH_WEEK

    if days==30:
        path_graph = PATH_GRAPH_MONTH

    os.makedirs('img', exist_ok=True)
    plt.savefig(path_graph, transparent=True, bbox_inches='tight')


if __name__ == '__main__':
    items = db.ExchangeRate.get_last_by(days=7)
    create_graph(items)
