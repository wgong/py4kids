import hashlib
import socket
import duckdb
import threading
from datetime import datetime
from typing import List, Any, Dict, Optional
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text
from sqlalchemy.engine.url import URL
import re

class SQLInterceptor:
    def __init__(self, duckdb_path: str = ":memory:"):
        """Initialize the SQL interceptor with DuckDB storage"""
        self.duckdb_conn = duckdb.connect(duckdb_path)
        self._setup_storage()
        self.local_data = threading.local()
        
    def _setup_storage(self):
        """Create the sql_info table in DuckDB"""
        self.duckdb_conn.execute("""
            CREATE TABLE IF NOT EXISTS sql_info (
                id INTEGER PRIMARY KEY,
                raw_sql_stmt TEXT,
                sql_stmt_hash VARCHAR(64),
                sql_stmt TEXT,
                param_names ARRAY(VARCHAR),
                param_values ARRAY(VARCHAR),
                sql_dialect VARCHAR(50),
                timestamp TIMESTAMP,
                caller_name VARCHAR(255),
                caller_ip VARCHAR(45)
            )
        """)
        
    def _get_caller_info(self) -> tuple[str, str]:
        """Get caller name and IP address"""
        caller_name = socket.gethostname()
        try:
            caller_ip = socket.gethostbyname(caller_name)
        except:
            caller_ip = "127.0.0.1"
        return caller_name, caller_ip

    def _cleanse_sql(self, sql: str) -> str:
        """Clean and normalize SQL statement"""
        # Remove comments
        sql = re.sub(r'--.*$', '', sql, flags=re.MULTILINE)
        sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
        
        # Normalize whitespace
        sql = re.sub(r'\s+', ' ', sql)
        sql = sql.strip()
        
        # Normalize quotation marks
        sql = re.sub(r'["""]', '"', sql)
        sql = re.sub(r"[''']", "'", sql)
        
        return sql

    def _extract_params(self, sql: str) -> tuple[str, List[str]]:
        """Extract parameter names from SQL statement"""
        # Match both :param and %(param)s style parameters
        named_params = re.findall(r':(\w+)|%\((\w+)\)s', sql)
        # Flatten the list of tuples and remove empty matches
        param_names = [name[0] or name[1] for name in named_params]
        
        # Replace parameters with standardized placeholder
        normalized_sql = re.sub(r':[^\s,)]+|%\(\w+\)s', '?', sql)
        
        return normalized_sql, param_names

    def _compute_hash(self, sql: str) -> str:
        """Compute hash of normalized SQL statement"""
        return hashlib.sha256(sql.encode()).hexdigest()

    def _format_param_value(self, value: Any) -> str:
        """Convert parameter value to string representation"""
        if value is None:
            return 'NULL'
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, (datetime, str)):
            return f"'{str(value)}'"
        elif isinstance(value, (list, tuple)):
            return f"ARRAY{str(value)}"
        return str(value)

    def create_engine_wrapper(self, url: str | URL, **kwargs) -> Engine:
        """Create a wrapped SQLAlchemy engine"""
        engine = create_engine(url, **kwargs)
        self._setup_engine_events(engine)
        return engine

    def _setup_engine_events(self, engine: Engine):
        """Set up event listeners for the engine"""
        @event.listens_for(engine, 'before_cursor_execute')
        def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            # Store original statement for access in after_cursor_execute
            self.local_data.statement = statement
            self.local_data.parameters = parameters

        @event.listens_for(engine, 'after_cursor_execute')
        def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            raw_sql = self.local_data.statement
            params = self.local_data.parameters or {}
            
            # Process SQL and parameters
            cleansed_sql = self._cleanse_sql(raw_sql)
            normalized_sql, param_names = self._extract_params(cleansed_sql)
            sql_hash = self._compute_hash(normalized_sql)
            
            # Get parameter values in same order as param_names
            param_values = []
            if isinstance(params, dict):
                param_values = [self._format_param_value(params.get(name)) for name in param_names]
            elif isinstance(params, (list, tuple)):
                param_values = [self._format_param_value(value) for value in params]

            # Get caller information
            caller_name, caller_ip = self._get_caller_info()
            
            # Store in DuckDB
            self.duckdb_conn.execute("""
                INSERT INTO sql_info (
                    raw_sql_stmt, sql_stmt_hash, sql_stmt, param_names, param_values,
                    sql_dialect, timestamp, caller_name, caller_ip
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                raw_sql,
                sql_hash,
                normalized_sql,
                param_names,
                param_values,
                engine.name,
                datetime.now(),
                caller_name,
                caller_ip
            ))

    def query_sql_info(self, conditions: str = "") -> List[Dict]:
        """Query the stored SQL information"""
        query = "SELECT * FROM sql_info"
        if conditions:
            query += f" WHERE {conditions}"
        query += " ORDER BY timestamp DESC"
        
        results = self.duckdb_conn.execute(query).fetchall()
        columns = [desc[0] for desc in self.duckdb_conn.description]
        
        return [dict(zip(columns, row)) for row in results]

# Usage Example
if __name__ == "__main__":
    # Initialize interceptor
    interceptor = SQLInterceptor()
    
    # Create wrapped engine
    engine = interceptor.create_engine_wrapper(
        "postgresql://user:pass@localhost:5432/dbname"
    )
    
    # Example queries that will be intercepted
    with engine.connect() as conn:
        # Simple query
        conn.execute(text("SELECT * FROM users WHERE id = :user_id"), 
                    {"user_id": 123})
        
        # More complex query
        conn.execute(text("""
            SELECT u.name, o.order_date 
            FROM users u 
            JOIN orders o ON u.id = o.user_id 
            WHERE u.status = :status AND o.amount > :min_amount
        """), {
            "status": "active",
            "min_amount": 1000
        })
    
    # Query stored SQL information
    recent_queries = interceptor.query_sql_info("timestamp > CURRENT_TIMESTAMP - INTERVAL '1 hour'")
    for query in recent_queries:
        print(f"SQL Hash: {query['sql_stmt_hash']}")
        print(f"Normalized SQL: {query['sql_stmt']}")
        print(f"Parameters: {query['param_names']} = {query['param_values']}")
        print("-" * 80)