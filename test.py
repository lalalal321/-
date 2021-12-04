# encoding: utf-8
"""
@author: zhou
@time: 2021/12/1 11:17
@file: test.py
@desc: 
"""

from util.neo4j_utils import *

if __name__ == '__main__':
    neo4j = Neo4j_Handle()
    print('--Neo4j connecting--')
    # neo4j.country_institution()
    # neo4j.institution_paper()
    neo4j.co_patent("tongji university")