"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
Last Modified: 2025-07-10
Version: 1.0
"""
from consumer import VisualTaskConsumer

def main():
    try:
        with VisualTaskConsumer() as consumer:
            consumer.process_tasks()
    except KeyboardInterrupt:
        print("\nExiting the application.")

if __name__ == "__main__":
    main()