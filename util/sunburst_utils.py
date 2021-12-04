from collections import defaultdict
import json


class Sunburst_Handle():
    def __init__(self):
        pass

    def list2dict(self, rank, IPCList):
        """
        :param rank: IPC分类的层数
        :param IPCList: 待分类的IPC列表
        :return:
        """
        tmpDict = defaultdict(list)
        for IPC in IPCList:
            if IPC:
                tmpDict[IPC[0:rank]].append(IPC)
        return tmpDict

    def last(self, father, myList):
        """
        :param father: IPC上一层分类结果
        :param myList: IPC分类统计
        """
        IPCDict = defaultdict(int)
        for IPC in myList:
            if IPC == father:
                continue
            IPCDict[IPC] += 1
        reList = []
        for key, value in IPCDict.items():
            tmpDict = {'name': key, 'value': value}
            reList.append(tmpDict)
        return reList

    def sunburst_process(self, IPC_list):
        """
        将数据整理成pyecharts需要的数据格式
        :param IPC_list:
        :return:
        """
        child = defaultdict(list)
        for IPC in IPC_list:
            if IPC:
                child[IPC[0]].append(IPC)
        children = []
        for key, value in child.items():
            tmpDict = {'name': key}
            # 大类 分类
            tmpDict01 = self.list2dict(3, value)
            children01 = []
            for key, value in tmpDict01.items():
                tmpDict02 = {'name': key, 'value': len(value)}
                # 小类 分类
                tmpDict03 = self.list2dict(4, value)
                children02 = []
                for key, value in tmpDict03.items():
                    tmpDict04 = {'name': key, 'value': len(value)}
                    # 大组 分类
                    tmpDict05 = self.list2dict(8, value)
                    children03 = []
                    for key, value in tmpDict05.items():
                        tmpDict06 = {'name': key}
                        if len(key) < 8:
                            continue
                        tmpDict06['value'] = len(value)
                        tmpDict06['children'] = self.last(tmpDict06['name'] + '00', value)
                        children03.append(tmpDict06)
                    children02.append(tmpDict04)
                    tmpDict04['children'] = children03
                children01.append(tmpDict02)
                tmpDict02['children'] = children02
            tmpDict['children'] = children01
            children.append(tmpDict)

        # with open("test.json", 'w', encoding='utf-8') as json_file:
        #     json.dump(children, json_file, ensure_ascii=False)
        return children


sun_burst = Sunburst_Handle()
