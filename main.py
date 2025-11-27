from logging import critical

from fontTools.misc.cython import returns

import table
from table import CriteriaPoint, PointCloud
from point_plotter import PointPlotter
import pandas as pd
from points_csv_handler import PointsCSVHandler
from img_handler import ImageHandler
import os
from collections import Counter

def report_1(points, distances, distance_in_r, r, count):

    # 1. exel report
    data = {
        'N': [i for i in range(len(points))],
        'class': [p.get_group_name() for p in points],
        'ends':[p.criteria[0] for p in points],
        'nodes': [p.criteria[1] for p in points],
        'R': [' ' for _ in range(len(points) - 1)] + [r],
        'dist_to_all': distances + [0],
        'dist_in_window': [' ' if i is None else i for i in distance_in_r] + [0],
    }
    count_named = {}
    for k, v in count.items():
        count_named[f'count_{k}'] = [' ' for _ in range(len(distances))] + [v]
    data.update(count_named)


    df = pd.DataFrame(data)

    df.to_excel('./report/report1/report_1.xlsx', index=False, sheet_name='Points')



    # tmp
    r_points = [*filter(lambda p: PointCloud.distance(p, points[-1]) <= r, points[:-1])]
    groups = Counter([p.get_group_name() for p in r_points])
    largest_group_amount  = max(groups.values())
    colours = [k for k, v in groups.items() if v == largest_group_amount]
    if colours:
        c_points = [p for p in r_points  if p.get_group_name() in colours]
        c_point = min(c_points, key=lambda p: PointCloud.distance(p, points[-1]))
    else:
        c_point = None

        # 2. plot report
    pp = PointPlotter('./report/report1/report_1.png')
    pp.plot_points_with_radius_groups(points, r, c_point)




def report_2(points, distances, distance_in_r, r, count):
    path_to_files = os.listdir('./data/data2/source_images') + [ImageHandler.img_name(points[-1].get_group_name())]
    group_names = map(lambda x: x.split('_')[0], path_to_files)

    data = {
        'N':[int(path.split('_')[-1].split('.')[0]) for path in path_to_files],
        'class': group_names,
        'path_to_file': path_to_files,
        'R':  [' ' for _ in range(len(points) - 1)] + [r],
        'dist_to_all': distances + [0],
        'dist_in_window': [' ' if i is None else i for i in distance_in_r] + [0],
    }
    count_named = {}
    for k, v in count.items():
        count_named[f'count_{k}'] = [' ' for _ in range(len(distances))] + [v]
    data.update(count_named)

    df = pd.DataFrame(data)
    df['_sort_prefix'] = df['path_to_file'].str.split('_').str[0]
    df['_sort_number'] = df['path_to_file'].str.split('_').str[1].str.split('.').str[0].astype(int)
    df = df.sort_values(by=['_sort_prefix', '_sort_number'])
    df = df.drop(['_sort_prefix', '_sort_number'], axis=1)
    df.to_excel('./report/report2/report_2.xlsx', index=False, sheet_name='Images')


def task1():
    # read source points
    criteria_points = PointsCSVHandler.read_points('./data/data1/points.csv')
    # load points to point cloud
    point_cloud = PointCloud(criteria_points, report_func=report_1)
    # create new point without belong to group

    new_cp = CriteriaPoint(list(map(int, input('Adding new point: (ends, nnodes)\n-> ').split())))
    # add this point to point cloud
    point_cloud.add(new_cp, float(input('radius = ')))
    # save this point (with already defined group) to csv
    PointsCSVHandler.update_points('./data/data1/points.csv', criteria_points)

def task2():
    # read source image and convert into criteria points
    source_folder_path = './data/data2/source_images'
    criteria_points = ImageHandler.read_folder(source_folder_path)
    # load points to point cloud
    point_cloud = PointCloud(criteria_points, report_func=report_2)
    # create new criteria point from test image
    test_folder_path = 'data/data2/test_images'
    test_img_paths = [os.path.join(test_folder_path, f) for f in os.listdir(test_folder_path)]
    [print(f'{i}. "{file_path}"') for i, file_path in enumerate(test_img_paths, start=1)]

    img_path = test_img_paths[int(input('-> ')) - 1]
    new_cp = ImageHandler.read_file(img_path)
    # add this point to point cloud
    group = point_cloud.add(new_cp, float(input('radius = ')))
    ImageHandler.add_img_to_source(img_path, group)




if __name__ == '__main__':
    value = input('1. Task 1\n2. Task 2\n3. Backup_1\n4. Backup_2\n-> ')
    match value:
        case "1":
            task1()
        case "2":
            task2()
        case "3":
            PointsCSVHandler.backup(15)
        case "4":
            ImageHandler.backup()
        case _:
            pass




