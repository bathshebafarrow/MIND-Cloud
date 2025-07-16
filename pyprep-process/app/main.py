"""
Author: Bathsheba Jackson
"""
from consumer import JobConsumer

def main():
    try:
        with JobConsumer() as consumer:
            consumer.process_messages()
    except KeyboardInterrupt:
        print("\nExiting the application.")

if __name__ == "__main__":
    main()