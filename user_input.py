from dataclasses import dataclass
import datetime

@dataclass
class GasUsageEntry:
    year: int
    day_of_year: int
    usage: float # gas usage in m³ or kwH

@dataclass
class DayWithUsage:
    day: int
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


def _convert_dates_to_days(usage_data: list[GasUsageEntry]) -> list[DayWithUsage]:
    """Converts GasUsageEntry data to DayWithUsage data. The first entry defines the year with days in [0,365). Entries in later years have days numbers >= 365
    
    Parameters:
        usage_data (list[GasUsageEntry]): List of GasUsageEntry objects.

    Returns:
        list[DayWithUsage]: List of DayWithUsage objects with continuous day numbering.
    """
    if not usage_data:
        return []
        
    base_year = usage_data[0].year
    converted_data = []
    for entry in usage_data:
        # days are counted from 0
        total_days = (entry.year - base_year) * 365 + entry.day_of_year - 1
        converted_data.append(DayWithUsage(total_days, entry.usage))
    
    return converted_data


def get_parsed_usage_data(file_path: str = "usage_data.txt") -> list[DayWithUsage]:
    """Reads and parses user gas usage data from textfile defined in file_path.
    
    Parameters:
        file_path (str): Path to the text file containing usage data.
        
    Returns:
        List[DayWithUsage]: A list of DayWithUsage objects for each intermediate gas meter reading.
    """
    raw_data = get_user_usage_data(file_path)
    parsed_data = []
    for date_str, usage in raw_data:
        year, day_of_year = parse_date(date_str)
        parsed_data.append(GasUsageEntry(year, day_of_year, usage))

    # sort data by year and day_of_year
    parsed_data.sort(key=lambda entry: (entry.year, entry.day_of_year))
    
    return _convert_dates_to_days(parsed_data)



if __name__ == "__main__":
    usage_data = get_user_usage_data()
    for date_str, usage in usage_data:
        print(f"Date: {date_str}, Usage: {usage:5.1f} m³")
