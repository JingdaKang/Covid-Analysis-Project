# Author:
###
 # @Author: Zhibiao Xie 980357; Jingda Kang 1276802; Haoxian Cai 1074429; Zihan Xu 1198129; Keyi Zhang 1217718
 # @Date: 2022-05-16 18:52:21
 # @LastEditTime: 2022-05-17 23:21:10
### 
# Zhibiao Xie 980357
# Jingda Kang 1276802
# Haoxian Cai 1074429
# Zihan Xu 1198129
# Keyi Zhang 1217718
# Last updated: 2022-5-17

#!/bin/bash

. ./unimelb-COMP90024-2022-grp-32-openrc.sh; ansible-playbook -i hosts --ask-become-pass nectar.yaml