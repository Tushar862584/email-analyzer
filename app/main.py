# In main.py
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime # <-- Add this import
from core.email_handler import process_emails
from core.logger import setup_logger

logger = setup_logger()

def job():
    logger.info("Starting Eliza email processing job...")
    process_emails()
    logger.info("Eliza job completed.")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    
    # Add next_run_time to run the job once at startup
    scheduler.add_job(job, 'interval', minutes=60, next_run_time=datetime.now())
    
    logger.info("Scheduler started. First run is immediate, then every 60 minutes.")
    scheduler.start()