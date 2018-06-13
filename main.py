#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


def input_map(x, y):
    map_list = []
    for j in range(y):
        x_list = input().split(" ")
        map_list.append(x_list)
    return map_list


def wallCreation(map_list):  # 壁の生成
    for i in range(len(map_list)):  # y
        map_list[i].insert(0, 1)  # y列x行の先頭に壁「1」挿入
        map_list[i].append(1)  # y列x行の末尾に壁「1」挿入

    wall_list = []
    for i in range(len(map_list[0])):  # x
        wall_list.append(1)
    map_list.insert(0, wall_list)  # y列の先頭に壁のリスト挿入
    map_list.append(wall_list)  # y列の末尾に壁のリスト挿入
    return map_list


def toStatusList(map_list):
    for i in range(len(map_list)):  # y
        for j in range(len(map_list[i])):  # x
            if(map_list[i][j] == 1 or map_list[i][j] == "1"):
                map_list[i][j] = "壁"  # 1を「wall」の「w」に変換
            elif(map_list[i][j] == "0"):
                map_list[i][j] = "空"  # ｓｔｒ"0"をintに変換
    return map_list


def set_scores(map_list, y, x, now_cost):
    ans = 0
    is_set = False
    if(map_list[y][x] == "空"):
        map_list[y][x] = now_cost + 1
        is_set = True
    elif(map_list[y][x] == "g"):
        ans = now_cost + 1
        print(ans)
        sys.exit()
    return map_list, is_set


def search_up_down_left_right(map_list, y, x):
    now_cost = map_list[y][x]
    is_set = False
    is_sets = [False, False, False, False]
    # 上
    map_list, is_sets[0] = set_scores(map_list, y-1, x, now_cost)
    # 下
    map_list, is_sets[1] = set_scores(map_list, y+1, x, now_cost)
    # 右
    map_list, is_sets[2] = set_scores(map_list, y, x+1, now_cost)
    # 左
    map_list, is_sets[3] = set_scores(map_list, y, x-1, now_cost)
    if(True in is_sets):
        is_set = True   # is_setsが一つでもTrueならis_setはTrue
    map_list[y][x] = "済"
    return map_list, is_set


# def get_max(map_list):
#     max_list = []
#     for i in range(len(map_list)):  # y列
#         max_list.append(map_list[i].max())
#     return max_list.max()


def get_distance_dijkstra(map_list):
    now_count = 0
    while(True):
        is_sets = False
        is_set = False
        for i in range(len(map_list)):  # y列
            for j in range(len(map_list[i])):  # x行
                if(map_list[i][j] == "s"):
                    map_list[i][j] = 0
                    map_list, is_set = \
                        search_up_down_left_right(map_list, i, j)
                    # print("x:" + str(j) + " y:" + str(i)
                    # + " is_set:" + str(is_set))
                elif(map_list[i][j] == now_count):
                    map_list, is_sets = \
                        search_up_down_left_right(map_list, i, j)
                    if(is_sets is True):
                        is_set = True
                    # print("x:" + str(j) + " y:" + str(i)
                    # + " is_set:" + str(is_set))
        if(is_set is False):
            print("Faile")
            sys.exit()
        now_count += 1


def map_show(map_list):
    for i in range(len(map_list)):  # y列
        print("")
        for j in range(len(map_list[i])):  # x行
            print(map_list[i][j], end="")


def main():
    xy = input().split(" ")
    x = int(xy[0])
    y = int(xy[1])
    map_list = input_map(x, y)
    map_list = wallCreation(map_list)
    map_list = toStatusList(map_list)
    get_distance_dijkstra(map_list)
    # map_show(map_list)


if __name__ == "__main__":
    main()
