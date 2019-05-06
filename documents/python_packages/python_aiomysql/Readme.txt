# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#   This is a document about aiomysql
#   You can learn:
#   1, Basic commands for aiomysql
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # #


#### easy work flow ####
conn = yield from aiomysql.connect(
host='127.0.0.1', 
port=3306,                                  
user='root', 
password='123456789', 
db='cza',
loop=loop)

yield from conn.cursor()

yield from cur.execute("SELECT Host,User FROM user")

yield from cur.fetchall()

yield from cur.close()

conn.close()


#### cursor way ####
# execute(query, args=None)
yield from cursor.execute("SELECT * FROM t1 WHERE id=%s", (5,))

# executemany(query, args)
data = [
    ('Jane','555-001'),
    ('Joe', '555-001'),
    ('John', '555-003')
   ]
stmt = "INSERT INTO employees (name, phone)
    VALUES ('%s','%s')"
yield from cursor.executemany(stmt, data)

# cur.fetchone()
# cur.fetchmany(size=None)
# cur.fetchall()
# cur.rowcount


# DictCursor
cursor = yield from conn.cursor(aiomysql.DictCursor)  -> if add this, result will be a dict, or else just data without key
# if you want to customize,overwrite aiomysql.DictCursor


# Pool
pool = yield from aiomysql.create_pool(
host='127.0.0.1', 
port=3306,
user='root', 
password='',
db='mysql', 
loop=loop, 
autocommit=False)

with (yield from pool) as conn:
    cur = yield from conn.cursor()
    yielf from cur.execute(sql)
    res = yield from cur.fetchone()
pool.close()
yield from pool.wait_closed()




