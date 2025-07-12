"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
"""
from consumer import JobConsumer

def main():
    try:
        with JobConsumer() as consumer:
            consumer.process_tasks()
    except KeyboardInterrupt:
        print("\nExiting the application.")

if __name__ == "__main__":
    main()