#!/usr/bin/bash

declare -a R
declare -a F
declare -a OLIGOS

R+=($1/*forward*)
F+=($1/*reverse*)
OLIGOS+=($2/*.txt)

# echo ${R[@]}
# echo ${F[@]}
# echo ${OLIGOS[@]}

