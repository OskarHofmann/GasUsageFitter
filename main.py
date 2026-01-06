from user_input import get_parsed_usage_data, GasUsageEntry
from fit_data import get_historic_data
from gas_usage_functions import fit_gas_usage_function


def split_usage_data_into_years(usage_data) -> list[list[GasUsageEntry]]:
    """
    Splits usage data into multiple lists if data spans multiple years (defined by duration not calendar years as heating periods usually span from autumn to spring).
    
    Parameters:
        usage_data (List[GasUsageEntry]): List of gas usage entries.

    Returns:
        List[List[GasUsageEntry]]: A list of lists, each containing gas usage entries spanning <= 365 days.
    """
    if not usage_data:
        return []

    split_data = []
    current_year = [usage_data[0]]
    start_of_current_year = usage_data[0]

    for entry in usage_data[1:]:
        if ((entry.year - start_of_current_year.year) * 365 + (entry.day_of_year - start_of_current_year.day_of_year)) <= 365:
            current_year.append(entry)
        else:
            split_data.append(current_year)
            current_year = [entry]
            start_of_current_year = entry

    if current_year:
        split_data.append(current_year)

    return split_data

    

if __name__ == "__main__":
    #get user data
    usage_data = get_parsed_usage_data()
    split_usage_data = split_usage_data_into_years(usage_data)
    
    # get gas usage function
    gas_usage_function = fit_gas_usage_function(get_historic_data(2024))

    def scaled_gas_usage_function(day: float, total_usage: float) -> float:
        return gas_usage_function(day) * total_usage

    print(usage_data)
    