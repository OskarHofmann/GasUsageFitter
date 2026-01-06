from .fit_data import get_historic_data

import numpy as np
import scipy.optimize
from collections.abc import Callable
import matplotlib.pyplot as plt

DAYS_PER_MONTH = np.array([31,28,31,30,31,30,31,31,30,31,30,31]) # assuming non-leap year
DAYS_PER_YEAR = DAYS_PER_MONTH.sum()

months = range(12)

def _integral_over_month(func: Callable[[int],float], month: int, days_per_month: np.ndarray) -> float:
    """Calculates the integral of a function of days over a specified month."""
    first_day = days_per_month[:month].sum() + 1
    last_day = days_per_month[:month+1].sum() + 1
    return np.trapz(np.array([func(x) for x in np.arange(first_day,last_day+1)]))

def _cumulative_integral_up_to_month(func: Callable[[int],float], month: int, days_per_month: np.ndarray) -> float:
    """Calculates the cumulative integral of a function of days up to the end of a specified month."""
    last_day = days_per_month[:month+1].sum() + 1
    return np.trapz(np.array([func(x) for x in np.arange(1,last_day+1)]))

def cumulative_integral_between_days(func: Callable[[int],float], start_day: int, end_day: int) -> float:
    """Calculates the cumulative integral of a function of days between two specified days."""
    if end_day < start_day:
        raise ValueError("end_day must be greater than or equal to start_day")
    
    integral = 0.0
    while end_day > DAYS_PER_YEAR:
        end_day -= DAYS_PER_YEAR
        integral += _cumulative_integral_up_to_month(func, 11, DAYS_PER_MONTH)
    return np.trapz(np.array([func(x) for x in np.arange(start_day,end_day+1)]))

def _gas_usage(day: float, s1, s2, s3, s4, c1, c2, c3, c4, offset) -> float:
    """Model function for gas usage as a function of day of the year. May lead to small "bump" in summer months due to higher order terms but overall fits well."""
    seasonal = s1 * np.sin(2 * np.pi * day / DAYS_PER_YEAR) + s2 * np.sin(4 * np.pi * day / DAYS_PER_YEAR) + s3 * np.sin(6 * np.pi * day / DAYS_PER_YEAR) + s4 * np.sin(8 * np.pi * day / DAYS_PER_YEAR)
    seasonal += c1 * np.cos(2 * np.pi * day / DAYS_PER_YEAR) + c2 * np.cos(4 * np.pi * day / DAYS_PER_YEAR) + c3 * np.cos(6 * np.pi * day / DAYS_PER_YEAR) + c4 * np.cos(8 * np.pi * day / DAYS_PER_YEAR)

    return seasonal + offset


def fit_gas_usage_function(share_per_month: np.ndarray, verbose: bool = False, plot: bool = False ) -> Callable[[float], float]:
    """Returns a fitted gas usage function based on the provided data of monthly gas usage shares.

    Parameters:
    share_per_month: The monthly share of gas usage to use for fitting.
    verbose (bool): If True, prints detailed fitting information.
    plot (bool): If True, generates plots of the fitted function and residuals.

    Returns:
    Callable[[float], float]: A function that takes a day of the year and returns the fitted gas usage (as yearly share per day). The function is periodic over [0, 365).  """

    def residuals(coefficients: np.ndarray) -> np.ndarray:
        res = np.zeros(12)
        for month in months:
            integral = _integral_over_month(lambda x: _gas_usage(x, *coefficients), month, DAYS_PER_MONTH)
            res[month] = integral - share_per_month[month]
        return res

    initial_guess = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0])
    popt = scipy.optimize.least_squares(residuals, initial_guess).x

    def fitted_gas_usage(day: float) -> float:
        return _gas_usage(day, *popt)
    
    if verbose:
         # Print share per months based on fitted function and compare to original shares
        print("Month | Original Share | Fitted Share")
        for month in months:
            fitted_share = _integral_over_month(fitted_gas_usage, month, DAYS_PER_MONTH)
            print(f"{month+1:5d} | {share_per_month[month]:14.6f} | {fitted_share:12.6f}")
        print("\nRemaining squared residuals:", np.sum(residuals(popt)**2))
        print("\nYearly integral of fitted function:", _cumulative_integral_up_to_month(fitted_gas_usage, 11, DAYS_PER_MONTH))
    
    if plot:
        # plot residuals
        res = residuals(popt)
        plt.bar(range(1, 13), res)
        plt.xlabel("Month")
        plt.ylabel("Residual")
        plt.title("Residuals of Fitted Gas Usage per Month")
        plt.show()

        # plot fitted function over the year
        days = np.arange(1, DAYS_PER_YEAR + 1)
        fitted_values = [fitted_gas_usage(day) for day in days]
        plt.plot(days, fitted_values)
        plt.xlabel("Day of Year")
        plt.ylabel("Fitted Gas Usage (yearly share per day)")
        plt.title("Fitted Gas Usage Over the Year")
        plt.show()
    
    return fitted_gas_usage


if __name__ == "__main__":

    fitted_gas_usage = fit_gas_usage_function(get_historic_data(2024), verbose=True, plot=True)



   

    

 