import time
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO)

class StreamMonitor:
    def __init__(self, stream):
        self.stream = stream

    def monitor(self):
        while True:
            line = self.stream.readline()  # Read a line from the stream
            if not line:
                break  # Exit on end of stream
            logging.info(f'New line: {line.strip()}')
            time.sleep(1)  # Simulate processing time

# Example usage: 
# if __name__ == '__main__':
#     with open('example.log', 'r') as log_file:
#         monitor = StreamMonitor(log_file)
#         monitor.monitor()