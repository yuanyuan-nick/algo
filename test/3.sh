#!/bin/bash
begin_date="2018-10-01"
a=`date -j -v +1d -f "%Y-%m-%d" $begin_date +%Y-%m-%d`
echo $a

