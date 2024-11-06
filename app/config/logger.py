from datetime import datetime
from loguru import logger
import os

if not os.path.exists('logs/error'):
    os.makedirs('logs/error')

if not os.path.exists('logs/info'):
    os.makedirs('logs/info')

today = datetime.today().strftime("%Y-%m-%d")

logger.add(f"logs/error/{today}.log", 
           rotation="00:00", 
           retention="30 days", 
           level="ERROR",
           )

logger.add(f"logs/info/{today}.log", 
           rotation="00:00", 
           retention="30 days", 
           level="INFO",
           )