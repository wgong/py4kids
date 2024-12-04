# Python examples using different database drivers and logging approaches

# 1. Using Python's built-in logging
import logging
import psycopg2
from psycopg2.extras import LoggingConnection

# Configure logging
logging.basicConfig(
    filename='sql.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# PostgreSQL with LoggingConnection
conn = psycopg2.connect(
    dsn="dbname=test user=postgres",
    connection_factory=LoggingConnection
)
conn.initialize(logging.getLogger('sql_logger'))

# 2. Custom wrapper class for any database connection
class LoggingDatabaseWrapper:
    def __init__(self, real_connection):
        self.real_connection = real_connection
        self.logger = logging.getLogger('sql_logger')
    
    def cursor(self):
        return LoggingCursorWrapper(self.real_connection.cursor(), self.logger)
    
    def __getattr__(self, attr):
        return getattr(self.real_connection, attr)

class LoggingCursorWrapper:
    def __init__(self, cursor, logger):
        self.cursor = cursor
        self.logger = logger
    
    def execute(self, sql, params=None):
        start_time = time.time()
        try:
            if params:
                self.logger.debug(f"Executing SQL: {sql} with params {params}")
                result = self.cursor.execute(sql, params)
            else:
                self.logger.debug(f"Executing SQL: {sql}")
                result = self.cursor.execute(sql)
            duration = time.time() - start_time
            self.logger.debug(f"Execution time: {duration:.2f} seconds")
            return result
        except Exception as e:
            self.logger.error(f"Error executing SQL: {sql}")
            self.logger.error(f"Error details: {str(e)}")
            raise
    
    def __getattr__(self, attr):
        return getattr(self.cursor, attr)

# 3. SQLAlchemy event-based logging
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
import time

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, params, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())
    logging.debug("SQL: %s" % statement)
    logging.debug("Parameters: %s" % str(params))

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, params, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop()
    logging.debug("Total Time: %.2f" % total)

# Create engine with logging
engine = create_engine('postgresql://user:pass@localhost/dbname')

# 4. JDBC-style proxy (Python example)
class ConnectionProxy:
    def __init__(self, real_connection):
        self.real_connection = real_connection
        self.logger = logging.getLogger('jdbc_style_logger')
        
    def prepare_statement(self, sql):
        self.logger.debug(f"Preparing statement: {sql}")
        start_time = time.time()
        stmt = self.real_connection.prepare_statement(sql)
        duration = time.time() - start_time
        self.logger.debug(f"Statement preparation time: {duration:.2f} seconds")
        return StatementProxy(stmt, sql, self.logger)

class StatementProxy:
    def __init__(self, real_statement, sql, logger):
        self.real_statement = real_statement
        self.sql = sql
        self.logger = logger
        
    def execute(self, *args):
        self.logger.debug(f"Executing: {self.sql}")
        self.logger.debug(f"Parameters: {args}")
        start_time = time.time()
        try:
            result = self.real_statement.execute(*args)
            duration = time.time() - start_time
            self.logger.debug(f"Execution time: {duration:.2f} seconds")
            return result
        except Exception as e:
            self.logger.error(f"Error executing: {self.sql}")
            self.logger.error(f"Error details: {str(e)}")
            raise

# 5. Integration with metrics collection
class MetricsLoggingCursor:
    def __init__(self, cursor, metrics_client):
        self.cursor = cursor
        self.metrics_client = metrics_client
    
    def execute(self, sql, params=None):
        start_time = time.time()
        try:
            result = self.cursor.execute(sql, params)
            duration = time.time() - start_time
            
            # Log metrics
            self.metrics_client.timing('sql.query.time', duration * 1000)
            self.metrics_client.increment('sql.query.count')
            
            # Categorize query type
            query_type = self._categorize_query(sql)
            self.metrics_client.increment(f'sql.query.type.{query_type}')
            
            return result
        except Exception as e:
            self.metrics_client.increment('sql.query.error')
            raise
    
    def _categorize_query(self, sql):
        sql = sql.strip().lower()
        if sql.startswith('select'):
            return 'select'
        elif sql.startswith('insert'):
            return 'insert'
        elif sql.startswith('update'):
            return 'update'
        elif sql.startswith('delete'):
            return 'delete'
        return 'other'