Python Mind Map
====================

Copyright (c) 2017-2018 Red Liu <lli_njupt@163.com>
Released under the MIT licence.

Python Mind Map based on Graphviz and yaml.

Yaml file to configure graph style and mind source file:

- In styles/ the style.yaml is used to configure dot graph. You can changed it to fix your own mind map.
- In sample/  sample.yaml is a source file example.

The sample output svg like below:

![An amazing tree](sample/sample.yaml.svg)



You can convert svg file to other formation with command:

`$ convert  -colorspace RGB -density 200 -quality 50 sample.yaml.svg sample.jpg`

If you want to output Chinese characters or more beautiful mind map, maybe you need to install new fonts, with linux just put them into /usr/share/fonts/.