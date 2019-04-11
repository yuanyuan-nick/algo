#!/bin/bash
begin_date="2019-04-01"
end_date="2019-04-04"
while [ $begin_date != $end_date ]
do 
/anaconda3/bin/python3.6 /Users/zy/Desktop/work/other/algo/replay_his.py $begin_date
begin_date=`date -j -v +1d -f "%Y-%m-%d" $begin_date +%Y-%m-%d`
echo $begin_date
done
