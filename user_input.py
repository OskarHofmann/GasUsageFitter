from dataclasses import dataclass
import datetime

@dataclass
class GasUsageEntry:
    year: int
    day_of_year: int
    usage: float # gas usage in m³ or kwH


def get_user_usage_data(file_path: str = "usage_data.txt"):
    """Reads user gas usage data from textfile defined in file_path.
    
    Parameters:
        file_path (str): Path to the text file containing usage data.
        
    Returns:
        List[Tuple[str, float]]: A list of tuples with date strings and usage values.
    """
    data = []
    with open(file_path, "r") as f:
        for line in f:
            date_str, usage_str = line.strip().split(' ')
            data.append((date_str, float(usage_str)))
    return data

def parse_date(date_str: str):
    """Parses a date string in the format 'YYYY-MM-DD' and returns a tuple of (year, day_of_year).
    
    Parameters:
        date_str (str): Date string in the format 'YYYY-MM-DD'.
        
    Returns:
        Tuple[int, int]: A tuple containing year and day_of_year as integers.

    """
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")

    return date_obj.year, date_obj.timetuple().tm_yday


def get_parsed_usage_data(file_path: str = "usage_data.txt") -> list[GasUsageEntry]:
    """Reads and parses user gas usage data from textfile defined in file_path.
    
    Parameters:
        file_path (str): Path to the text file containing usage data.
        
    Returns:
        List[GasUsageEntry]: A list of GasUsageEntry objects for each intermediate gas meter reading.
    """
    raw_data = get_user_usage_data(file_path)
    parsed_data = []
    for date_str, usage in raw_data:
        year, day_of_year = parse_date(date_str)
        parsed_data.append(GasUsageEntry(year, day_of_year, usage))
    return parsed_data



if __name__ == "__main__":
    usage_data = get_user_usage_data()
    for date_str, usage in usage_data:
        print(f"Date: {date_str}, Usage: {usage:5.1f} m³")
