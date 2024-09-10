import sqlite3

def query_table_name(conn):
    # 创建一个游标对象，它将用于执行 SQL 命令
    cursor = conn.cursor()
    # 执行查询语句，从 sqlite_master 表中选择所有表名
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # 获取查询结果
    tables = cursor.fetchall()
    # 打印结果
    for table in tables:
        print(table[0])
    # 关闭游标和连接
    cursor.close()


def query_task_table(conn):
    # 创建一个游标对象，它将用于执行 SQL 命令
    cursor = conn.cursor()
    # 执行查询语句
    cursor.execute("SELECT * FROM task")
    # 获取查询结果
    results = cursor.fetchall()

    # 打印结果
    for row in results:
        print(row)
    # 关闭游标和连接
    cursor.close()

if __name__ == '__main__':
    # 连接到数据库（如果数据库不存在，将会创建一个新的数据库）
    conn = sqlite3.connect('tasks.db')
    query_table_name(conn)
    query_task_table(conn)
    conn.close()