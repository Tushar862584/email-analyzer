# Main entry point
print('Eliza AI automation starting...')
from core.email_handler import process_emails
from core.logger import setup_logger
from apscheduler.schedulers.blocking import BlockingScheduler

logger = setup_logger()

def job():
    logger.info("Starting Eliza email processing job...")
    process_emails()
    logger.info("Eliza job completed.")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', minutes=60)
    logger.info("Scheduler started. Running every 60 minutes.")
    scheduler.start()