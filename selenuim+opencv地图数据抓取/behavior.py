# coding:utf-8

#!/usr/bin/env python
# coding:utf-8
import RGB
import keepprogress as kp

# 3N-54N 0.2
# 73E-136E 0.4
tar = []

i = 3
while i <= 54:
    j = 73
    while j <= 136.2:
        tar.append([i, j])
        j += 0.4
        j = round(j, 1)
    i += 0.2
    i = round(i, 1)

site = []
for i in range(0,256):
    if i % 2 == 0:
        site += tar[i*159:(i+1)*159]
    else:
        site += tar[i*159:(i+1)*159][::-1]
    if i != 0:
        print(site[i*159-1:i*159+2])
eaa = []
for i in site:
    eaa.append(str(i[0])+'°N'+'|'+str(i[1])+'°E')





