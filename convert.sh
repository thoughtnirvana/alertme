#creates insert into statement for all the stock values.

IFS=$'\n'
v=`cat StockCodes`
a="INSERT INTO "
b="stocks_stock"
c=" VALUES("
e=", 'BSE');"
for i in $v
do
  d=$i
  echo $a$b$c$d$e >> db.sql
done
