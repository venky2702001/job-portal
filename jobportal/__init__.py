import pymysql

# Django's mysql backend expects the MySQLdb (mysqlclient) driver, which
# needs native compilation. PyMySQL is pure Python and drop-in compatible,
# which makes builds on hosts like Render much simpler.
pymysql.install_as_MySQLdb()
