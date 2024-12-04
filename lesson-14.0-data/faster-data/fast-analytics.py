import re
import json
import time
from collections import defaultdict
from typing import Dict, List, Any
from dataclasses import dataclass
from queue import Queue
import threading

@dataclass
class SQLEvent:
    sql: str
    params: tuple
    timestamp: float
    duration: float
    database: str
    user: str
    application: str

class BusinessMetricsExtractor:
    def __init__(self):
        self.patterns = {
            'new_order': re.compile(r'INSERT\s+INTO\s+orders.*', re.IGNORECASE),
            'product_view': re.compile(r'SELECT.*FROM\s+products.*', re.IGNORECASE),
            'inventory_update': re.compile(r'UPDATE\s+inventory.*', re.IGNORECASE),
            'user_signup': re.compile(r'INSERT\s+INTO\s+users.*', re.IGNORECASE)
        }
        
        self.metric_handlers = {
            'new_order': self._handle_order,
            'product_view': self._handle_product_view,
            'inventory_update': self._handle_inventory,
            'user_signup': self._handle_signup
        }

    def _handle_order(self, sql: str, params: tuple) -> Dict[str, Any]:
        # Extract order details from INSERT INTO orders... SQL
        try:
            # Example: Match columns and values
            columns = re.findall(r'INSERT\s+INTO\s+orders\s*\((.*?)\)', sql)[0].split(',')
            return {
                'event_type': 'new_order',
                'columns': columns,
                'values': params
            }
        except Exception:
            return None

    def _handle_product_view(self, sql: str, params: tuple) -> Dict[str, Any]:
        # Extract product view patterns from SELECT... FROM products... SQL
        try:
            product_id = re.findall(r'WHERE\s+product_id\s*=\s*[?]', sql)
            return {
                'event_type': 'product_view',
                'product_id': params[0] if params else None
            }
        except Exception:
            return None

    def analyze_sql(self, event: SQLEvent) -> Dict[str, Any]:
        for pattern_name, pattern in self.patterns.items():
            if pattern.match(event.sql):
                handler = self.metric_handlers.get(pattern_name)
                if handler:
                    result = handler(event.sql, event.params)
                    if result:
                        result.update({
                            'timestamp': event.timestamp,
                            'duration': event.duration,
                            'database': event.database
                        })
                        return result
        return None

class RealTimeAnalytics:
    def __init__(self):
        self.metrics = defaultdict(int)
        self.time_series = defaultdict(list)
        self.lock = threading.Lock()
        self.event_queue = Queue()
        self.extractor = BusinessMetricsExtractor()
        
        # Start background processing
        self.processing_thread = threading.Thread(target=self._process_events)
        self.processing_thread.daemon = True
        self.processing_thread.start()

    def _process_events(self):
        while True:
            event = self.event_queue.get()
            self._analyze_event(event)
            self.event_queue.task_done()

    def _analyze_event(self, event: SQLEvent):
        metrics = self.extractor.analyze_sql(event)
        if metrics:
            with self.lock:
                event_type = metrics['event_type']
                self.metrics[event_type] += 1
                self.time_series[event_type].append({
                    'timestamp': event.timestamp,
                    'value': metrics
                })
                
                # Keep only last hour of data
                cutoff = time.time() - 3600
                self.time_series[event_type] = [
                    x for x in self.time_series[event_type] 
                    if x['timestamp'] > cutoff
                ]

    def add_event(self, event: SQLEvent):
        self.event_queue.put(event)

    def get_metrics(self) -> Dict[str, Any]:
        with self.lock:
            return {
                'counters': dict(self.metrics),
                'recent_events': {
                    k: v[-10:] for k, v in self.time_series.items()
                }
            }

class SQLAnalyticsWrapper:
    def __init__(self, real_connection, analytics: RealTimeAnalytics):
        self.real_connection = real_connection
        self.analytics = analytics
        self.db_info = {
            'database': real_connection.info.dbname,
            'user': real_connection.info.user,
            'application': real_connection.info.application_name
        }

    def cursor(self):
        return SQLAnalyticsCursor(
            self.real_connection.cursor(),
            self.analytics,
            self.db_info
        )

class SQLAnalyticsCursor:
    def __init__(self, cursor, analytics: RealTimeAnalytics, db_info: Dict[str, str]):
        self.cursor = cursor
        self.analytics = analytics
        self.db_info = db_info

    def execute(self, sql: str, params=None):
        start_time = time.time()
        try:
            result = self.cursor.execute(sql, params or ())
            duration = time.time() - start_time
            
            # Create and analyze SQL event
            event = SQLEvent(
                sql=sql,
                params=params or (),
                timestamp=start_time,
                duration=duration,
                database=self.db_info['database'],
                user=self.db_info['user'],
                application=self.db_info['application']
            )
            self.analytics.add_event(event)
            
            return result
        except Exception as e:
            # Still track failed queries
            duration = time.time() - start_time
            event = SQLEvent(
                sql=sql,
                params=params or (),
                timestamp=start_time,
                duration=duration,
                database=self.db_info['database'],
                user=self.db_info['user'],
                application=self.db_info['application']
            )
            self.analytics.add_event(event)
            raise

# Example usage
if __name__ == "__main__":
    analytics = RealTimeAnalytics()
    
    # Simulate some SQL events
    events = [
        SQLEvent(
            sql="INSERT INTO orders (user_id, total) VALUES (?, ?)",
            params=(1, 99.99),
            timestamp=time.time(),
            duration=0.1,
            database="shop",
            user="app",
            application="web"
        ),
        SQLEvent(
            sql="SELECT * FROM products WHERE product_id = ?",
            params=(123,),
            timestamp=time.time(),
            duration=0.05,
            database="shop",
            user="app",
            application="web"
        )
    ]
    
    for event in events:
        analytics.add_event(event)
    
    # Get real-time metrics
    print(json.dumps(analytics.get_metrics(), indent=2))