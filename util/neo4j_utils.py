"""
@desc: py2neo连接以及查询方法
"""

from collections import defaultdict

from py2neo import Graph
from util.sunburst_utils import sun_burst
from util.charts_utils import *


class Neo4j_Handle:

    def __init__(self):
        self.sun_burst = sun_burst
        self.graph = Graph("bolt: // localhost:7687", auth=("neo4j", "123"))
        print("Neo4j Init ...")

    def institution_patent(self, number=10):
        """
        统计各机构的专利数量，按照专利发表数量绘制柱形图
        :param number: 柱形图显示的机构个数
        :return: None
        """
        query = 'MATCH (n:institution) RETURN n.Institution AS key,size((:Patent)-[:Institution_patent]->(n:institution)) AS value ORDER BY value DESC'
        chart_data = self.search(query, number)
        line_draw(chart_data, title="机构-专利数量图")

    def IPC_sunburst(self, institution="barry wehmiller company inc"):
        """
        绘制机构发表的所有专利的IPC分布旭日图
        :param institution: 需要查询的机构名称，暂不支持模糊查询
        :return: None
        """
        query = 'MATCH (n:Patent)-[r:Institution_patent]-(m:institution{Institution:"' + institution + '"}) with n MATCH (n)-[r:Patent_IPC]->(m:IPC) RETURN m.IPC AS IPC'
        chart_data = self.search_sunburst(query)
        sunburst_draw(chart_data, title=institution + "专利IPC旭日图")

    def co_patent(self, institution=""):
        """
        绘制机构与其他机构专利合作节点图
        :param institution: 需要查询的机构名称
        :return: None
        """
        query = 'MATCH (a:institution{Institution:"' + institution + '"})-[r:Institution_cooperation_patent]->(b:institution) RETURN a.Institution AS source,r,b.Institution AS target'
        nodes, links = self.search_graph(query, institution)
        if nodes:
            graph_draw(nodes, links, title=institution + "专利合作节点图")
        else:
            print("没有该机构的相关数据")

    # 查找并返回字典
    def search(self, query, number):
        record_dict = defaultdict(int)
        cursor = self.graph.run(query)
        while cursor.forward() and number > 0:
            record = cursor.current
            number -= 1
            key = record.get("key")
            value = record.get("value")
            record_dict[key] = value
        return record_dict

    # 返回绘制机构专利旭日图所需的数据
    def search_sunburst(self, query):
        IPC_list = []
        cursor = self.graph.run(query)
        while cursor.forward():
            record = cursor.current
            IPC_list.append(record.get("IPC"))
        # 将数据处理为旭日图所需格式
        if not IPC_list:
            return None
        return self.sun_burst.sunburst_process(IPC_list)

    # 返回绘制节点图所需的数据
    def  search_graph(self, query, institution):
        nodes, links = [], []
        nodeset = set()
        cursor = self.graph.run(query)
        while cursor.forward():
            record = cursor.current
            source = record.get("source")
            target = record.get("target")
            nodeset.add(source)
            nodeset.add(target)
            #节点图 关系数据整理
            links.append({"source": source, "target": target})
        #节点图 节点数据整理
        for node in nodeset:
            #当节点为查询的机构时，为该节点设置不同的颜色与大小
            if node == institution:
                nodes.append(
                    {"name": node,
                     "draggable": "true",
                     "itemStyle": {'color': "#6e7074"},
                     "symbolSize": 50
                     }
                )
                continue

            nodes.append(
                {"name": node,
                 "draggable": "true",
                 "itemStyle": {'color': "#61a0a8"}
                 }
            )
        if not nodes:
            return None, None
        return nodes, links



