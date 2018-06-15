#!/usr/bin/env python
# -*- coding: utf-8 -*-


def input_map(x, y):
    map_list = []
    for j in range(y):
        x_list = input().split(" ")
        map_list.append(x_list)
    return map_list


def wallCreation(map_list):  # リスト外への探索を防ぐため、マップの周りに壁を生成するメソッド
    for i in range(len(map_list)):  # y
        map_list[i].insert(0, 1)  # y列x行の先頭に壁「1」挿入
        map_list[i].append(1)  # y列x行の末尾に壁「1」挿入

    wall_list = []
    for i in range(len(map_list[0])):  # x
        wall_list.append(1)
    map_list.insert(0, wall_list)  # y列の先頭に壁のリスト挿入
    map_list.append(wall_list)  # y列の末尾に壁のリスト挿入
    return map_list


def toStatusList(map_list):  # 通れる道の「0」を「□」に、通れない壁の「1」を「■」に変えるメソッド
    for i in range(len(map_list)):  # y
        for j in range(len(map_list[i])):  # x
            if(map_list[i][j] == 1 or map_list[i][j] == "1"):
                map_list[i][j] = "■"  # 1を壁の ■ に変換
            elif(map_list[i][j] == "0"):
                map_list[i][j] = "□"  # 0を空の □ に変換
    return map_list


def set_scores(map_list, y, x, now_cost):  # 通れる道かゴールならコストを入れるメソッド
    goal_x = 0
    goal_y = 0
    is_set = False
    if(map_list[y][x] == "□"):
        map_list[y][x] = now_cost + 1
        is_set = True
    elif(map_list[y][x] == "g"):
        map_list[y][x] = now_cost + 1
        is_set = True
        goal_x = x
        goal_y = y
    return map_list, is_set, goal_y, goal_x


def search_up_down_left_right(map_list, y, x):  # 上下右左の道にコストを入れるメソッド
    # print("up_down_left_right X:"+str(x)+" Y:"+str(y))
    now_cost = map_list[y][x]
    is_set = False
    is_sets = [False, False, False, False]
    goals_x = [0, 0, 0, 0]
    goals_y = [0, 0, 0, 0]
    goal_x = 0
    goal_y = 0
    # 上
    map_list, is_sets[0], goals_y[0], goals_x[0] = set_scores(map_list, y-1, x,
                                                              now_cost)
    # 下
    map_list, is_sets[1], goals_y[1], goals_x[1] = set_scores(map_list, y+1, x,
                                                              now_cost)
    # 右
    map_list, is_sets[2], goals_y[2], goals_x[2] = set_scores(map_list, y, x+1,
                                                              now_cost)
    # 左
    map_list, is_sets[3], goals_y[3], goals_x[3] = set_scores(map_list, y, x-1,
                                                              now_cost)
    if(True in is_sets):
        is_set = True   # is_setsが一つでもTrueならis_setはTrue
    if(4 != goals_y.count(0)):
        goal_y = sum(goals_y)
    if(4 != goals_x.count(0)):
        goal_x = sum(goals_x)
    map_list[y][x] = str(map_list[y][x])
    return map_list, is_set, goal_y, goal_x


def get_distance_dijkstra(map_list):  # ゴールまでのコストとゴールの座標を返すメソッド
    now_cost = 0
    goal_x = 0
    goal_y = 0
    cost_until_a_goal = 0
    while(True):
        is_sets = False
        is_set = False
        for i in range(len(map_list)):  # y列
            for j in range(len(map_list[i])):  # x行
                if(map_list[i][j] == "s"):
                    map_list[i][j] = 0
                    map_list, is_set, goal_y, goal_x = \
                        search_up_down_left_right(map_list, i, j)
                    print("x:" + str(j) + " y:" + str(i) + " is_set:" +
                          str(is_set))
                    if(goal_y != 0 or goal_x != 0):
                        break
                elif(map_list[i][j] == now_cost):
                    map_list, is_sets, goal_y, goal_x = \
                        search_up_down_left_right(map_list, i, j)
                    print("x:" + str(j) + " y:" + str(i) + " is_set:" +
                          str(is_sets))
                    if(is_sets is True):
                        is_set = True
                    if(goal_y != 0 or goal_x != 0):
                        break
            if(goal_y != 0 or goal_x != 0):
                break
        if(is_set is False):
            cost_until_a_goal = "Fail"
            break
        if(goal_x != 0 or goal_y != 0):
            cost_until_a_goal = map_list[goal_y][goal_x]
            break
        now_cost += 1
    return cost_until_a_goal, goal_y, goal_x


def map_show(map_list):
    for i in range(len(map_list)):  # y列
        for j in range(len(map_list[i])):  # x行
            print(map_list[i][j], end=" ")
        print("")  # 改行


# ゴールの座標からスタートまでの道順を逆探索するメソッド
def directions_to_goal(map_list, goal_y, goal_x):
    directions_to_goal_list = {}
    directions_to_goal_list.update({int(map_list[goal_y][goal_x]): []})
    directions_to_goal_list[int(map_list[goal_y][goal_x])].append([goal_x,
                                                                  goal_y])
    # print("directions_to_goal_list["+str(map_list[goal_y][goal_x])+"]")
    for i in reversed(range(int(map_list[goal_y][goal_x]))):
        directions_to_goal_list.update({i: []})
        for j in range(len(map_list)):  # y列
            for k in range(len(map_list[j])):  # x行
                if(map_list[j][k] == str(i) or map_list[j][k] == i):
                    # print("directions_to_goal_list["+str(i+1)+"]")
                    # print(directions_to_goal_list[i+1])
                    if([k, j-1] in directions_to_goal_list[i+1] or  # 上
                       [k, j+1] in directions_to_goal_list[i+1] or  # 下
                       [k+1, j] in directions_to_goal_list[i+1] or  # 右
                       [k-1, j] in directions_to_goal_list[i+1]):  # 左
                        directions_to_goal_list[i].append([k, j])
                        if("0" == map_list[j][k]):
                            map_list[j][k] = "s"
                        else:
                            map_list[j][k] = "+"
    map_list[goal_y][goal_x] = "g"
    return directions_to_goal_list


def directions_show(directions_to_goal_list):
    for i in range(len(directions_to_goal_list)):
        for j in range(len(directions_to_goal_list[i])):
            print("コスト：" + str(i) + ", X：" +
                  str(directions_to_goal_list[i][j][0]) +
                  ", Y："+str(directions_to_goal_list[i][j][1]))


def main():
    print("タイルマップ上のSTART地点からGOAL地点までの最短経路の座標、道順、距離を出力します。")
    print("ｘ軸（横軸）のマスの数を入力してください：", end="")
    x = int(input())
    print("ｙ軸（縦軸）のマスの数を入力してください：", end="")
    y = int(input())
    print(str(x) + " × " + str(y) + " のマップ入力してください。\n"
          "入力例(ｘ軸 3 , ｙ軸 2)の場合")
    print("s 1 g")
    print("0 0 0")
    print("通れる道：0 ,通れない壁：1 ,START地点：s ,GOAL地点：g ,と表現します。")
    print("※ｘ軸は上記のように空白を挟んでください。")
    print("※ｓとｇを入力していいのは 1 回だけです。")
    map_list = input_map(x, y)
    map_list = wallCreation(map_list)
    map_list = toStatusList(map_list)
    print("\n探索開始")
    cost_until_a_goal, goal_y, goal_x = get_distance_dijkstra(map_list)
    print("\n探索完了")
    map_show(map_list)
    if(cost_until_a_goal == "Fail"):
        print("\nゴールにたどり着くことはできませんでした")
    else:
        directions_to_goal_list = directions_to_goal(map_list,
                                                     goal_y, goal_x)
        print("\nゴールまでの座標を表示します")
        directions_show(directions_to_goal_list)
        print("\nゴールまでの道順を「+」で表示します")
        map_show(map_list)
        print("\nゴールまでの距離は " + str(cost_until_a_goal) + " マス分です。")


if __name__ == "__main__":
    main()
