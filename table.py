import typing
import math
from collections import Counter

class PointCloud:
    def __init__(self, points, report_func=None):
        self.points = points
        self.report_func = report_func

    @staticmethod
    def distance(p1, p2):
        summation = 0.0
        for c1, c2 in zip(p1.get_criteria(), p2.get_criteria()):
            diff = float(c1) - float(c2)
            summation += diff * diff
        distance = math.sqrt(summation)
        return distance


    def __exel_report(self, distance, distance_in_r, r, count):
        self.report_func(self.points, distance, distance_in_r, r, count)
        pass




    def add(self, new_point, radius):

        # find points in radius distance
        distances = []
        distances_in_r = [None for _ in range(len(self.points))]

        for i, p in enumerate(self.points):
            distance = PointCloud.distance(p, new_point)
            distances.append(distance)
            if distance < radius:
                point_dist = (p, distance)
                distances_in_r[i] = point_dist

        count = Counter(p_d[0].get_group_name() for p_d in distances_in_r if p_d is not None)

        max_group_count = max(count.values())
        max_groups = set(filter(lambda x: count[x] == max_group_count, count.keys()))
        if len(max_groups) != 1:
            nearest_p = min([*filter(lambda x: x is not None and x[0].get_group_name() in max_groups, distances_in_r)], key=lambda x: x[1])
            group_name = nearest_p[0].get_group_name()

        else:
            group_name = list(max_groups)[0]

        new_point.set_group_name(group_name)

        # update
        self.points.append(new_point)
        # report
        if self.report_func is not None:
            self.__exel_report(distances, [None if i is None else i[1] for i in distances_in_r], radius, count)

        return group_name









class CriteriaPoint:

    def __init__(self, criteria, group_name=None):
        self.criteria = criteria
        self.group_name = group_name

    def get_criteria(self):
        return self.criteria

    def get_group_name(self):
        return self.group_name

    def set_group_name(self, group_name):
        self.group_name = group_name

    def __repr__(self):
        return f"CriteriaPoint: {self.group_name}, {self.criteria}"

