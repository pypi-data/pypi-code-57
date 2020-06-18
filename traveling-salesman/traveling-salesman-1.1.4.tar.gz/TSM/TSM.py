import sys
from typing import List

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("TkAgg")
DEBUG = False
pause_interval = 0.01


class Node:
    def __init__(self, x: float, y: float, disolate: list):
        self.x = x
        self.y = y
        self.disolate = disolate

    def __str__(self):
        return 'X:{},Y:{},Disolate:{}'.format(self.x, self.y, self.disolate)

    def distance(self, node):
        from scipy.spatial import distance
        a = self.x, self.y
        b = node.x, node.y
        return distance.euclidean(a, b)




def greedy(nodes: list, start_index: int = 0, end_index=None, plot=False, plot_annotate=True):
    # list of travelled cities
    my_travel_book = []
    if DEBUG:
        print('traveler\'s start point : ', start_index)
    # initialize travel book data with start index and end index
    my_travel_book.append(start_index)
    my_travel_book.append(end_index)

    # distance vector referance for start index
    dist = np.array([nodes[start_index].distance(i) for i in nodes])

    # first plot data for drawing cities
    x = [node.x for node in nodes]
    y = [node.y for node in nodes]
    if plot:
        fig, ax = plt.subplots()

        # first plot that contains cities

        # second plot that contains route

        line1, = ax.plot(x, y, 'r.')
        fig.suptitle('Greedy Algorithm')

        if plot_annotate:
            # draw all names for cities
            for i in range(len(x)):
                ax.annotate(str(i), (x[i], y[i]))

        line2, = ax.plot(x, y, 'b--')
        plt.draw()
        # sum of travel distance
    sum_of_distance = 0
    while len(my_travel_book) < len(nodes):
        # masked_dist is excluded(non-zeros and not contains travelled cities) list of distance matrix
        if len(my_travel_book) > 0:
            mask = np.ones(len(dist), np.bool)
            mask[my_travel_book] = 0
            masked_dist = dist[mask]
        else:
            masked_dist = dist
        # assign nearest point to variable
        min_val_idx = np.where(dist == np.min(masked_dist))[0][0]
        next_point = nodes[min_val_idx]
        if DEBUG:
            print('traveler\'s next point :{} value:{} '.format(min_val_idx, dist[min_val_idx]))
        sum_of_distance = sum(
            [nodes[my_travel_book[i]].distance(nodes[my_travel_book[i - 1]]) for i in range(1, len(my_travel_book))]

        )
        plt.title('sum of distance : {}'.format(sum_of_distance))
        # adding data to travel list but not last index its inserting before to last
        my_travel_book.insert(-1, min_val_idx)
        # update distance matrix for nex iteration
        dist = np.array([nodes[min_val_idx].distance(i) for i in nodes])
        if DEBUG:
            print(my_travel_book)
        # update second plot x and y data and draw except last destination cause its final
        if plot:
            line2.set_xdata([nodes[i].x for i in my_travel_book[:-1]])
            line2.set_ydata([nodes[i].y for i in my_travel_book[:-1]])
            plt.draw()
            plt.pause(pause_interval)

    if plot:
        line2.set_xdata([nodes[i].x for i in my_travel_book])
        line2.set_ydata([nodes[i].y for i in my_travel_book])
        plt.show()
    return my_travel_book, sum_of_distance


def smallest_increase(nodes: list, start_index: int = 0, end_index=-1, plot=False, plot_annotate=True) -> [list, float]:
    # list of travelled cities
    my_travel_book = []
    if DEBUG:
        print('traveler\'s start point : ', start_index)

    # initialize travel book data with start index and end index
    my_travel_book.append(start_index)
    # if end index <0 its going to be wrong named in travel list this clause for fix this
    if end_index >= 0:
        my_travel_book.append(end_index)

    # first plot data for drawing cities
    x = [node.x for node in nodes]
    y = [node.y for node in nodes]
    if plot:
        fig, ax = plt.subplots()
        # first plot that contains cities
        # second plot that contains route
        line1, = ax.plot(x, y, 'r.')
        fig.suptitle('Smallest Increase Algorithm')

        # draw all names(labels) for cities
        if plot_annotate:
            for i in range(len(x)):
                ax.annotate(str(i), (x[i], y[i]))

        line2, = ax.plot(x, y, 'b--')
        plt.draw()

    # first plot that contains cities
    # second plot that contains route

    # sum of travel distance
    sum_of_distance = 0

    for p in range(len(nodes)):
        index = 0

        if len(my_travel_book) != 0:
            smallest_increase = sys.maxsize

            for i in range(1, len(my_travel_book)):
                # distance value Start to End (A to B)
                orj_d = nodes[my_travel_book[i]].distance(nodes[my_travel_book[i - 1]])
                # distance value Start to P + P to End (A to P to B)
                new_d = nodes[p].distance(nodes[my_travel_book[i]]) + nodes[p].distance(nodes[my_travel_book[i - 1]])
                # if p in my_travel_book:
                #     continue
                if new_d - orj_d <= smallest_increase:
                    smallest_increase = new_d - orj_d
                    index = i
        my_travel_book.insert(index, p)
        sum_of_distance = sum(
            [nodes[my_travel_book[i]].distance(nodes[my_travel_book[i - 1]]) for i in range(1, len(my_travel_book))]
        )
        if plot:
            plt.title('sum of distance : {}'.format(sum_of_distance))
            line2.set_xdata([nodes[i].x for i in my_travel_book[:-1]])
            line2.set_ydata([nodes[i].y for i in my_travel_book[:-1]])
            plt.draw()
            plt.pause(pause_interval)

    if plot:
        line2.set_xdata([nodes[i].x for i in my_travel_book])
        line2.set_ydata([nodes[i].y for i in my_travel_book])
        plt.show()
    return my_travel_book, sum_of_distance


def read_all(data='resources/sehir_xy.txt') -> list:
    # reading data for xy coordinates
    with open(data) as data:
        sehir_data = data.readlines()
    # reading distance matrix data
    # with open(disolate) as data:
    #     disolate_data = data.readlines()
    nodes: List[Node] = []
    for s in sehir_data:
        # node x data
        s_x, s_y = map(float, s.split())
        # node y data
        # an instance of integer vector(list) of distance matrix
        # s_distance_v = list(map(float, s_disolate.strip().split()))
        # adding nodes to return list
        nodes.append(Node(s_x, s_y, []))

    return nodes


def find_closest_path(travellers_book: list, start_point: int, end_point: int, plot=False, suptitle='Find Closest Path',
                      show_route=False) -> float:
    travellers_book = np.array(travellers_book)
    start_idx = np.where(travellers_book == start_point)[0][0]
    end_idx = np.where(travellers_book == end_point)[0][0]

    if start_idx < end_idx:
        result_book = travellers_book[start_idx:end_idx + 1]
    else:
        result_book = travellers_book[end_idx:start_idx + 1]
    distance = sum(
        [nodes[result_book[i]].distance(nodes[result_book[i - 1]]) for i in range(1, len(result_book))]
    )
    if plot:
        # first plot data for drawing cities
        x = [node.x for node in nodes]
        y = [node.y for node in nodes]
        ax = plt.plot()
        # first plot that contains cities
        # second plot that contains route
        ax, = plt.plot(x, y, 'k.')
        plt.suptitle(suptitle)
        plt.title('Distance between {} and {} is {} km'.format(start_point, end_point, distance))

        # draw all names(labels) for cities
        for i in range(len(x)):
            plt.annotate(str(i), (x[i], y[i]))
        if show_route:
            x = [nodes[node].x for node in travellers_book]
            y = [nodes[node].y for node in travellers_book]
            line3, = plt.plot(x, y, 'b--')
        x = [nodes[node].x for node in result_book]
        y = [nodes[node].y for node in result_book]
        line2, = plt.plot(x, y, 'r-')

        plt.show()

    return distance


# if __name__ == '__main__':
#     nodes = read_all('resources/sehir_xy.txt')
#
#     # # plot update interval
#     pause_interval = 0.000000000000000000000000000001
#     # # if debug is true its printing bunch of stuff on console
#     # DEBUG = True
#     #
#     # # when start index doesnt assigned a value its select 0 index in list
#     start_idx = 45
#     # end index required just for smallest_increase when it doesnt assign a value its select last point on list
#     end_idx = 51
#
#     # plot gostermek icin plot true
#     # smallest_book, _ = smallest_increase(nodes, start_idx, end_idx, plot=True, plot_annotate=True)
#     greedy_book, _ = greedy(nodes, start_idx, end_idx, plot=True)
#     # sehirlerin rotasini gostermek icin show_route = True parametresi girilmelidir
#     # find_closest_path(greedy_book, 12, 5, plot=True)
#     # find_closest_path(smallest_book, 12, 5, plot=True, show_route=True, suptitle='Smallest Increase Algorithm Route')
#
#     # result.csv ye algoritmalarin baslangic ve bitis noktalarina bagli olarak zaman ve uzaklik sonuclarini yazdirir
#     # Compare()
