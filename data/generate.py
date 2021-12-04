# encoding: utf-8
"""
@author: zhou
@time: 2021/7/12 14:55
@file: generate.py
@desc: 生成neo4j的导入语句,在ne4j/bin下运行即可导入
"""

import os


def import_gen(database_name=None):
    """
    导入语句生成
    :param database_name: 数据库名称，默认为neo4j
    :return: None
    """
    link, label = "", ""
    path = os.getcwd()
    # print(path)
    for file in os.listdir("link"):
        file = " --relationships " + path + '\\link\\' + file
        # print(file)
        link += file

    for file in os.listdir("label"):
        file = " --nodes " + path + '\\label\\' + file
        # print(file)
        label += file

    if database_name:
        code = "neo4j-admin import -- database " + database_name + label + link
    else:
        code = "neo4j-admin import" + label + link
    f = open("neo4j.txt", "w", encoding="utf-8")
    f.write(code)


if __name__ == '__main__':
    import_gen()

# neo4j-admin import
# --nodes
# --relationships
