import app.validators.shared_validator as shared_validator
from app.config.logger import logger
import re

#Validate user ip address upon registration and login
def validate_ip(ip: str):
    logger.info("Validating user IP address")
    
    ipv4_pattern = re.compile(
        r'^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$'
    )
    ipv6_pattern = re.compile(
        r'^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^(::(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4})$'
    )
    
    if not ipv4_pattern.match(ip) and not ipv6_pattern.match(ip):
        logger.info(f"{ip}")
        logger.warning(f"User IP address does not match any pattern: {ip}")
        raise shared_validator.ValidationException("Invalid IP address")
    
    logger.info(f"{ip}")
    logger.info("User IP validation passed")