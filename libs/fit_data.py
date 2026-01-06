import numpy as np

def get_din_data():
    """
    use relative gas usage based on German "Gradtagszahlentabelle" according to DIN 4713
    https://de.wikipedia.org/wiki/DIN_4713

    Returns:
    np.ndarray: Array of monthly shares of gas usage based on "Gradtagszahlentabelle".
    """
    share_per_month = np.array([170,150,130,80,40,40/3,40/3,40/3,30,80,120,160])
    share_per_month /= 1000
    return share_per_month

# historic data for gas usage for households in Germany (currently only 2024 available)
# https://www.smard.de/page/home/topic-article/211972/214592/gasverbrauch
supported_years_for_historic_data = [2024]
historic_data = {
    2024: np.array([1191,1085,987,686,309,151,143,143,158,452,980,1259])
}

def get_historic_data(year:int=2024):
    """
    use historic data for gas usage
    
    Parameters:
    year (int): The year for which to retrieve historic gas usage data.

    Returns:
    np.ndarray: Array of monthly shares of gas usage for the specified year.
    """

    if year not in supported_years_for_historic_data:
        raise ValueError(f"Historic data for year {year} is not supported. Supported years: {supported_years_for_historic_data}")
    
    share_per_month = historic_data[year]
    share_per_month = share_per_month / share_per_month.sum()
    
    return share_per_month