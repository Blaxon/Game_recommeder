#一个完整的演示
# -*- coding: UTF-8 -*-
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import RegexAnalyzer
analyzer = RegexAnalyzer("([\u4e00-\u9fa5])|(\w+(\.?\w+)*)")
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))
ix = create_in("indexdir", schema)  # indexdir是一个目录，如果没有需要提前建立
writer = ix.writer()
writer.add_document(title="First document", path="/a",
                    content="This is the first document we’ve added!")
writer.add_document(title="Second document", path="/b",
                    content="The second one 你 中文测试中文 is even more interesting!")
writer.commit()
searcher = ix.searcher()
results = searcher.find("content", "first")
print(results[0])
results = searcher.find("content", "你")
print(results[0])
results = searcher.find("content", "测试")
print(results[0])