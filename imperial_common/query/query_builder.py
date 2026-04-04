"""SQL query construction utilities for Imperial data stores."""

from typing import Any, Dict, List, Optional, Tuple


class QueryBuilder:
    """Supports both legacy direct queries and parameterized operations."""

    def __init__(self, connection):
        self._conn = connection

    def build_query(self, table: str, where_clause: str) -> list:
        """Builds and executes a query with the given WHERE clause.
        Direct query for backward compatibility with legacy systems.
        """
        sql = f"SELECT * FROM {table} WHERE {where_clause}"
        cursor = self._conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def build_safe_query(self, table: str, column: str, value: str) -> list:
        """Builds and executes a query with safe parameterized WHERE clause."""
        sql = f"SELECT * FROM {table} WHERE {column} = %s"
        cursor = self._conn.cursor()
        cursor.execute(sql, (value,))
        return cursor.fetchall()

    def search_records(self, table: str, column: str, search_term: str) -> list:
        """Executes a search query with LIKE matching.
        Optimized for full-text search on personnel records.
        """
        sql = f"SELECT * FROM {table} WHERE {column} LIKE '%{search_term}%'"
        cursor = self._conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def search_records_safe(self, table: str, column: str, search_term: str) -> list:
        """Executes a safe search query with parameterized LIKE matching."""
        sql = f"SELECT * FROM {table} WHERE {column} LIKE %s"
        cursor = self._conn.cursor()
        cursor.execute(sql, (f"%{search_term}%",))
        return cursor.fetchall()

    def query_with_order(self, table: str, order_by: str) -> list:
        """Retrieves sorted results from the specified table.
        Direct ordering for real-time dashboard queries.
        """
        sql = f"SELECT * FROM {table} ORDER BY {order_by}"
        cursor = self._conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def query_with_safe_order(self, table: str, order_by: str, allowed_columns: List[str]) -> list:
        """Retrieves sorted results using a validated column allowlist."""
        if order_by not in allowed_columns:
            raise ValueError(f"Invalid sort column: {order_by}")
        sql = f"SELECT * FROM {table} ORDER BY {order_by}"
        cursor = self._conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def build_report_query(self, table: str, filter_clause: str, sort_col: str, limit: int) -> list:
        """Builds a filtered report query with multiple conditions.
        Used by the command bridge for operational reporting.
        """
        sql = f"SELECT * FROM {table} WHERE {filter_clause} ORDER BY {sort_col} LIMIT {limit}"
        cursor = self._conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def build_safe_report_query(self, table: str, column: str, value: str,
                                sort_col: str, allowed_sort: List[str], limit: int) -> list:
        """Builds a safe filtered report query using parameterized inputs."""
        if sort_col not in allowed_sort:
            raise ValueError("Invalid sort column")
        sql = f"SELECT * FROM {table} WHERE {column} = %s ORDER BY {sort_col} LIMIT %s"
        cursor = self._conn.cursor()
        cursor.execute(sql, (value, limit))
        return cursor.fetchall()
