"""Event Processor for Real-Time Analytics

Processes incoming events from Redis stream and updates metrics.
"""

import redis
import json
import time
from datetime import datetime
import threading

class EventProcessor:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.running = False
        
    def process_event(self, event_data):
        """Process a single event and update metrics"""
        try:
            event_type = event_data.get('event_type')
            user_id = event_data.get('user_id')
            timestamp = event_data.get('timestamp', datetime.utcnow().isoformat())
            
            # Update event counters
            self.redis_client.incr(f'counter:{event_type}:today')
            self.redis_client.incr('counter:total_events')
            
            # Track active users
            self.redis_client.sadd('active_users:current', user_id)
            self.redis_client.setex(f'user:last_seen:{user_id}', 3600, timestamp)
            
            # Update events per minute counter
            minute_key = f'events:minute:{datetime.now().strftime("%Y%m%d%H%M")}'
            self.redis_client.incr(minute_key)
            self.redis_client.expire(minute_key, 3600)
            
            print(f"Processed event: {event_type} for user {user_id}")
            return True
            
        except Exception as e:
            print(f"Error processing event: {e}")
            return False
    
    def consume_stream(self):
        """Continuously consume events from Redis stream"""
        last_id = '0'
        print("Event processor started. Listening for events...")
        
        while self.running:
            try:
                # Read from stream
                streams = self.redis_client.xread(
                    {'events:stream': last_id},
                    count=10,
                    block=1000
                )
                
                if streams:
                    for stream_name, messages in streams:
                        for message_id, event_data in messages:
                            self.process_event(event_data)
                            last_id = message_id
                            
            except Exception as e:
                print(f"Stream consumption error: {e}")
                time.sleep(1)
    
    def start(self):
        """Start the event processor"""
        self.running = True
        thread = threading.Thread(target=self.consume_stream)
        thread.daemon = True
        thread.start()
        print("Event processor thread started")
    
    def stop(self):
        """Stop the event processor"""
        self.running = False
        print("Event processor stopped")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  Real-Time Event Processor")
    print("  Processing events from Redis stream...")
    print("="*60 + "\n")
    
    processor = EventProcessor()
    processor.start()
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        processor.stop()
