Python Mind Map
====================

Copyright (c) 2017-2018 Red Liu <lli_njupt@163.com>
Released under the MIT licence.

Python Mind Map based on Graphviz and yaml.

Yaml files are used to configure graph style and mind source file:

- styles/style.yaml is used to configure dot graph. You can changed it to fix your own mind map.
- sample/sample.yaml is a source file example.

Pymindmap focuses on creating mindmap automatically with same style defined in styles/xxx.yaml.

The sample output svg looks like below:

![An amazing tree](sample/sample.yaml.origin.svg)



With tapered.yaml style looks like:

![tapered](sample/sample.yaml.tapered.svg)

With tapered.yaml style  and LR direction looks like:

![LR](sample/sample.tapered.LR.svg)

You can convert svg file to other formation with command:

`$ convert  -colorspace RGB -density 200 -quality 50 sample.yaml.svg sample.jpg`

If you want to output Chinese characters or more beautiful mind map, maybe you need to install new fonts, with linux just put them into /usr/share/fonts/.

And you can create your own style yaml files under styles folder  as templates.

---

#graphivz 相关资料

graphivz 文档：

- https://graphviz.gitlab.io/documentation/
- https://graphviz.readthedocs.io/en/stable/manual.html
- http://soc.if.usp.br/manual/graphviz/html/

Dot 中文语法参考：

- https://www.jianshu.com/p/e44885a777f0
- https://blog.csdn.net/jy692405180/article/details/52077979

graphivz 示例：

1. http://www.tonyballantyne.com/graphs.html
2. https://graphs.grevian.org/example
3. http://statistics.ohlsen-web.de/sem-path-diagram/
4. https://renenyffenegger.ch/notes/tools/Graphviz/examples/index
5. https://martinfowler.com/bliki/AlignmentMap.html

DiagrammeR 是对 graphviz 扩展。

graphviz 通过算法进行节点自动排版处理，使用直线连接通常不会出现重叠问题，但是在曲线时有以下缺陷：

- 边长不会根据标签长度自动增长
- 边可能与其它边或者节点重合
- 标签文字可能位于边的底层，被边的线条遮挡
- 每一行或列（rank）的节点只能居中对齐，无法左右对齐

由于AT&T官方不再投入，且自动布局涉及到NP非多项式时间问题，以上缺陷短时间内无法解决，参考：https://softwarerecs.stackexchange.com/questions/40/alternative-for-graphviz-with-better-automatic-node-placement-for-large-graphs。

---

#dot 相关命令

dot 转换命令：

dot test.dot -Tsvg -o out.svg

dot -Granksep=0.3 -Gnodesep=0.2 -Tsvg -o overlap.svg overlap.dot # 这些参数很有用

图像（通常是边线）重叠的一些解决方法：

- **edge concentrators** (concentrate=true): Merge  multiple edges with a common endpoint into single edges, and have  partially parallel edges share parts of their path.
- **ports** : Edges can have their origin and endpoint on  a specific port (n, ne, e, se, s, sw, w, nw, w, c, _). Depending on the  edge ports, the edge changes its form (spline).
- **invisible nodes** : There may be cases where introducing invisible nodes to route edges can have the desired effect.

neato 是另一个转换命令，布局不同，其他命令还有：

```
  neato - filter for drawing undirected graphs
  twopi - filter for radial layouts of graphs
  circo - filter for circular layout of graphs
  fdp - filter for drawing undirected graphs
  sfdp - filter for drawing large undirected graphs
  patchwork - filter for tree maps
  # 这些命令都是指向 dot 的软连接，提供不同的布局
```

man 是一个好工具，在文档最后通常会给出参考资料链接，这些信息对深入理解命令的原理和用法非常有用。这些资料中通常也会给出参考文档，这些文档整体上构成一个有向图，它们就是构建该程序的技术基础资料集合。

