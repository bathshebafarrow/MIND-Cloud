from app.config import SQS_URL
from worker import FileQueueWorker

def processQueue():
    with FileQueueWorker(SQS_URL) as worker:
        worker.process_queue()

if __name__ == "__main__":
    processQueue()
