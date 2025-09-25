from typing import Optional

import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool


_pool: Optional[MySQLConnectionPool] = None


def init_connection_pool(host: str, user: str, password: str, database: str, pool_name: str, pool_size: int) -> None:
    global _pool
    if _pool is None:
        _pool = MySQLConnectionPool(
            pool_name=pool_name,
            pool_size=pool_size,
            host=host,
            user=user,
            password=password,
            database=database,
            autocommit=False,
        )


def get_connection():
    if _pool is None:
        raise RuntimeError("Database pool is not initialized. Call init_connection_pool first.")
    return _pool.get_connection()


def execute_query(query: str, params: tuple = (), fetchone: bool = False, fetchall: bool = False):
    connection = get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        result = None
        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()
        connection.commit()
        return result
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


