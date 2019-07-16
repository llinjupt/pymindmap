#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""
Tools for drawing simple mind mapping based on Graphivz.
Depend on pygraphviz and yaml

Copyright (c) 2017-2018 Red Liu <lli_njupt@163.com>

Released under the MIT licence.
"""
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import pygraphviz as pgv

def load_yaml(file):
  import yaml
  try:
    from yaml import CLoader as Loader, CDumper as Dumper
  except ImportError:
    from yaml import Loader, Dumper
    
  with open(file, 'r') as fr:
    readed = fr.read()
    return yaml.load(readed, Loader=Loader)
  
  return None

def set_graph_attr(G, style='styles/style.yaml'):
  style = load_yaml(style)
  
  if style is None:
    # 通常不要设定图片大小，而由 dot 自动计算得到比较好的布局图片，
    # 对生成图片缩放得到目标图片
    #G.graph_attr['size']='4,4'
    
    G.graph_attr['encoding']='utf-8'
    
    # ratio，与 size 配合使用来确定图像尺寸和布局
    # ratio=x, height/width 的比例为 x，如果设定 size，则保证长边不超过size设定
    #G.graph_attr['ratio']='0.5'
    # ratio=fill 表示正好填充 size 指定的变长大小
    # 此外还有 compress 和 auto 选项
    
    # 输出图像位于图片正中
    G.graph_attr['center']='true'
    
    G.graph_attr['overlap']='false'
    
    # 旋转
    #G.graph_attr['rotate']='90'
    #G.graph_attr['orientation']="landscape"
    
    G.graph_attr['concentrate']='true'
    G.graph_attr['rank']='sink'
    
    # 绘图方向
    G.graph_attr['rankdir']='BT'

    # 绘图顺序，边应该位于最底层
    G.graph_attr['outputorder']='edgesfirst'
    #G.graph_attr['label']="sample"
    
    # 边的线条类型：curved,polyline,ortho,spline,none...
    G.graph_attr['splines']='curved'
    
    # node separation: 相同行(BT/TB)或列(LR/RL)上的相邻节点间最小距离
    G.graph_attr['nodesep']="0.2"
    
    # rank separation: 行或列之间的做小距离，将影响连接两个节点的边的长度
    G.graph_attr['ranksep']="0.5"    

    G.node_attr['shape']='rect'
    G.node_attr['fixedsize']='false'
    G.node_attr['width']=0.5
    G.node_attr['height']=0.1
    G.node_attr['fontcolor']='black'
    G.node_attr['fontsize']='12'
    #G.node_attr['fontname']='楷体'
    G.node_attr['fontname']='Regular'
    G.node_attr['fillcolor']='#fafafa'
    G.node_attr['style']='rounded,filled,setlinewidth(0.5)'
    
    G.edge_attr['color']='slategray3'
    G.edge_attr['style']='setlinewidth(6),tapered'
    G.edge_attr['arrowhead']='orinv'
    G.edge_attr['fontname']='Regular'
    G.edge_attr['fontsize']='11'
    G.edge_attr['fontcolor']='darkslategray'
    
    # 标签文字连接到边线，默认 false
    #G.edge_attr['decorate']='true'
    #G.edge_attr['constraint']='true'
  else:
    graph = style.get('graph', '')
    if graph != '':
      for item in graph:
        for key in item.keys():
          G.graph_attr[key] = str(item[key])
          
    node = style.get('node', '')
    if node != '':
      for item in node:
        for key in item.keys():
          G.node_attr[key] = str(item[key])

    edge = style.get('edge', '')
    if edge != '':
      for item in edge:
        for key in item.keys():
          G.edge_attr[key] = str(item[key])
  
# analyse -> for xlabel
# return label,xlabel
def create_xlabel(label):
  labels = label.split('->')
  if len(labels) == 2:
    return (''.join(labels[1:])).strip(), labels[0].strip()
  
  return label.strip(), ""

# if parent exist then also create edge
def create_node_edge(G, parent, label, level=0):
  lab,xlabel = create_xlabel(str(label))    
  if parent != None:
    realp,_ = create_xlabel(parent)
    if xlabel == '':
      G.add_edge(realp, lab, samehead="h1", sametail="t1")
    else:
      G.add_edge(realp, lab, xlabel=xlabel, samehead="h1", sametail="t1")        
  G.add_node(lab)

def create_dict_node(G, parent, dic, level=0):
  assert(type(dic) == dict)
  
  for item in dic:      
    val = dic[item]
    typ = type(val)
    
    label = item
    if typ == dict:
      create_dict_node(G, item, val, level + 1)
    elif typ == list:
      create_list_node(G, item, val, level + 1)
    else:
      label = str(item) + ':' + str(val)
    
    create_node_edge(G, parent, label, level)

    # Note: only handle first item
    #break 

def create_list_node(G, parent, lis, level=0):
  assert(type(lis) == list)
  
  for li in lis:
    typ = type(li)
    if typ == dict:
      create_dict_node(G, parent, li, level + 1)
    else:
      create_node_edge(G, parent, li, level)

def create_graph(G, yamlfile):
  dic = load_yaml(yamlfile)
  if dic is not None:
    create_dict_node(G, None, dic, 0)

def create_dot_file(yamlfile, style='styles/style.yaml'):
  # directed means draw a directed graph with arrow edges
  G = pgv.AGraph(name="Sample", directed=True)
  
  # init style
  set_graph_attr(G, style=style)  
  
  # create graph
  create_graph(G, yamlfile)
  
  # create dot file
  G.layout(prog='dot')
  G.draw(path = yamlfile + ".dot", format="dot")
  
  return G

def create_svg_file(yamlfile, style='styles/style.yaml'):
  G = create_dot_file(yamlfile, style=style)
  G.draw(path = yamlfile + ".svg", format="svg")
  return G

create_dot_file("sample/sample.yaml")
create_svg_file("sample/sample.yaml")

# 默认生成的 jpg 质量不高，svg 转 jpg，-resize 180 可调整图片大小
# convert  -colorspace RGB -density 200 -quality 50 sample.yaml.svg sample.jpg
