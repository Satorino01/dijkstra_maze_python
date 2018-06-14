#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
                map_list[i][j] = "■"  # 1を壁の ■ に変換
            elif(map_list[i][j] == "0"):
                map_list[i][j] = "□"  # 0を空の □ に変換
    return map_list


def set_scores(map_list, y, x, now_cost):
    is_set = False
    cost_until_a_goal = 0
    if(map_list[y][x] == "□"):
        map_list[y][x] = now_cost + 1
        is_set = True
    elif(map_list[y][x] == "g"):
        map_list[y][x] = now_cost + 1
        cost_until_a_goal = now_cost + 1
        is_set = True
    return map_list, is_set, cost_until_a_goal


def search_up_down_left_right(map_list, y, x):
    now_cost = map_list[y][x]
    is_set = False
    is_sets = [False, False, False, False]
    cost_until_a_goal = 0
    is_goals = [0, 0, 0, 0]
    # 上
    map_list, is_sets[0], is_goals[0] = set_scores(map_list, y-1, x, now_cost)
    # 下
    map_list, is_sets[1], is_goals[1] = set_scores(map_list, y+1, x, now_cost)
    # 右
    map_list, is_sets[2], is_goals[2] = set_scores(map_list, y, x+1, now_cost)
    # 左
    map_list, is_sets[3], is_goals[3] = set_scores(map_list, y, x-1, now_cost)
    if(True in is_sets):
        is_set = True   # is_setsが一つでもTrueならis_setはTrue
    if(4 != is_goals.count(0)):
        cost_until_a_goal = sum(is_goals)
        print("ゴール")
    map_list[y][x] = str(map_list[y][x])
    return map_list, is_set, cost_until_a_goal


# def get_max(map_list):
#     max_list = []
#     for i in range(len(map_list)):  # y列
#         max_list.append(map_list[i].max())
#     return max_list.max()


def get_distance_dijkstra(map_list):
    now_cost = 0
    cost_until_a_goal = 0
    while(True):
        is_sets = False
        is_set = False
        for i in range(len(map_list)):  # y列
            for j in range(len(map_list[i])):  # x行
                if(map_list[i][j] == "s"):
                    map_list[i][j] = 0
                    map_list, is_set, cost_until_a_goal = \
                        search_up_down_left_right(map_list, i, j)
                    if(cost_until_a_goal != 0):
                        return cost_until_a_goal
                    print("x:" + str(j) + " y:" + str(i) + " is_set:" +
                          str(is_set))
                elif(map_list[i][j] == now_cost):
                    map_list, is_sets, cost_until_a_goal = \
                        search_up_down_left_right(map_list, i, j)
                    if(cost_until_a_goal != 0):
                        return cost_until_a_goal
                    if(is_sets is True):
                        is_set = True
                    print("x:" + str(j) + " y:" + str(i) + " is_set:" +
                          str(is_sets))
        if(is_set is False):
            cost_until_a_goal = "Fail"
            break
        now_cost += 1
    return cost_until_a_goal


def map_show(map_list):
    for i in range(len(map_list)):  # y列
        print("")  # 改行
        for j in range(len(map_list[i])):  # x行
            print(map_list[i][j], end=" ")
    print("")  # 改行


def main():
    print("ダイクストラ法で盤面のSTART地点からGOAL地点までのコストを出します。")
    print("x軸（横軸）のマスの数を入力してください：", end="")
    x = int(input())
    print("y軸（縦軸）のマスの数を入力してください：", end="")
    y = int(input())
    print("マップを入力してください。入力例(x軸 3 , y軸 2)の場合：")
    print("s 1 g")
    print("0 0 0")
    print("通れる道：0 ,通れない壁：1 ,START地点：s ,GOAL地点：g ,と表現します")
    print("ｘ軸は上記のように空白を挟んで " + str(x) + " マス分の属性を入力してください,"
          "それを " + str(y) + " 行分繰り返してください。")
    print(" s と g を入力していいのは一回だけです：")
    map_list = input_map(x, y)
    map_list = wallCreation(map_list)
    map_list = toStatusList(map_list)
    cost_until_a_goal = get_distance_dijkstra(map_list)
    map_show(map_list)
    print("ゴールまでのコスト：" + str(cost_until_a_goal))


if __name__ == "__main__":
    main()
