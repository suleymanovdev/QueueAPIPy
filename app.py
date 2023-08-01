from fastapi import FastAPI, Query, BackgroundTasks
from rabbitmq_methods import send_username_to_queue
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get('/api/user/')
def get_user(username: str = Query(..., min_length=1), background_tasks: BackgroundTasks = BackgroundTasks()):
    logger.info(f"Received request for username: {username}")
    background_tasks.add_task(send_username_to_queue, username)
    return {'detail': f'{username} sent to the queue for processing.'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1234)
