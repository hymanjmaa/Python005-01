# 1
```sql
set character_set_database = utf8mb4;
set character_set_server = utf8mb4;
show variables like '%character%';

create database testdb;
create user xiao_ma; 
GRANT ALL PRIVILEGES ON testdb.* TO xiao_ma@"%" IDENTIFIED BY 'jiushipassword' WITH GRANT OPTION;
flush privileges; 
```

# 2  
```
见 homework.py 中 homework_2()
```

# 3
```
5    SELECT DISTINCT player_id, player_name, count(*) as num 
1    FROM player JOIN team ON player.team_id = team.team_id 
2    WHERE height > 1.80 
3    GROUP BY player.team_id 
4    HAVING num > 2 
6    ORDER BY num DESC 
7    LIMIT 2
```

# 4
```
select table1.id, table1.name, table2.id, table2.name from table1 inner join table2 on table1.id = table2.id;
1	 table1_table2	1	table1_table2

select table1.id, table1.name, table2.id, table2.name from table1 left join table2 on table1.id = table2.id;
1	 table1_table2	1	table1_table2
2	 table1 	NULL	NULL

select table1.id, table1.name, table2.id, table2.name from table1 right join table2 on table1.id = table2.id;
1	 table1_table2	1	table1_table2
NULL	NULL	3	table2
```

# 5
```
ALTER table table1 ADD INDEX idx_id(id);
CREATE INDEX idx_name ON table1 (name);

查询速度没有增加
每一个索引在 InnoDB 里面对应一棵 B+ 树
基于非主键索引的查询需要多扫描一棵索引树

SHOW INDEX FROM table_name; 查看索引
primary key: 一种特殊的唯一索引，不允许有空值。一般是在建表的时候同时创建主键索引。注意：一个表只能有一个主键。
unique: 唯一索引列的值必须唯一，但允许有空值。如果是组合索引，则列值的组合必须唯一。
index: 最基本的索引，它没有任何限制。
组合索引: 一个索引包含多个列，多用于避免回表查询。
全文索引 FULLTEXT: 全文检索。
索引一经创建不能修改，如果要修改索引，只能删除重建

适合索引的列是出现在where子句中的列，或者连接子句中指定的列
基数较小的类，索引效果较差，没有必要在此列建立索引
使用短索引，如果对长字符串列进行索引，应该指定一个前缀长度，这样能够节省大量索引空间
不要过度索引。索引需要额外的磁盘空间，并降低写操作的性能。
在修改表内容的时候，索引会进行更新甚至重构，索引列越多，这个时间就会越长。所以只保持需要的索引有利于查询即可

```

# 6
```
见 homework.py 中 homework_6()
```