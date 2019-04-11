#!/bin/bash
begin_date="2019-01-25"
end_date="2019-02-01"
while [ $begin_date != $end_date ]
do
begin_date=date -d "$begin_date +1 day " +"%Y-%m-%d"
echo $begin_date
done
