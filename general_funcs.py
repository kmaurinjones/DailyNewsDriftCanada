from datetime import datetime, date, timedelta
from dateutil import parser

def get_today_iso():
    """
    Get the current date in ISO format.
    
    Returns:
        str: The current date as a string in the format 'YYYY-MM-DD'.
        
    Examples:
        >>> get_today_iso()
        '2023-08-15'
    """
    return date.today().isoformat()

def robust_parse_date(date_string):
    """
    Robustly parses a date string and returns the date in ISO format. 
    Utilizes fuzzy parsing to handle various date formats.
    
    Args:
        date_string (str): The date string to be parsed.
        
    Returns:
        str: The parsed date as a string in the format 'YYYY-MM-DD'.
    
    Raises:
        ValueError: If the date_string can't be parsed.
        
    Examples:
        >>> robust_parse_date("Aug 15, 2023")
        '2023-08-15'
    """
    # Attempt to parse the date_string
    dt = parser.parse(date_string, fuzzy=True)
    
    # Return the date in the ISO format
    return dt.date().isoformat()

def get_date_str(date_str):
    """
    Converts a date string in the format 'YYYY-MM-DD' to a more readable format 'Mon DD, YYYY'.
    
    Args:
        date_str (str): The date string in the format 'YYYY-MM-DD'.
        
    Returns:
        str: The date in the format 'Mon DD, YYYY'.
    
    Raises:
        ValueError: If the input date string is not in the 'YYYY-MM-DD' format.
        
    Examples:
        >>> get_date_str("2023-08-15")
        'Aug 15, 2023'
    """
    # Parse the input date string to a datetime object
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    
    # Format the datetime object to the desired output format
    return date_obj.strftime('%b %d, %Y')

def get_time_minus_4h():
    now = datetime.now()
    four_hours_ago = now - timedelta(hours=4)
    time_minus_4h = four_hours_ago.strftime("%H:%M:%S")
    date_of_time_minus_4h = four_hours_ago.strftime("%Y-%m-%d")
    return date_of_time_minus_4h, time_minus_4h