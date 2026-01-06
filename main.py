from libs.user_input import get_parsed_usage_data, GasUsageEntry
from libs.fit_data import get_historic_data
from libs.gas_usage_functions import fit_gas_usage_function, integral_between_days

from dataclasses import dataclass
import matplotlib.pyplot as plt

if __name__ == "__main__":
    #get user data
    usage_data = get_parsed_usage_data("example_usage_data.txt")
    
    # get gas usage function
    gas_usage_function = fit_gas_usage_function(get_historic_data(2024))
    yearly_integral = integral_between_days(gas_usage_function, 0, 365)

    # for each pair of consecutive entries, calculate the scaling factor between gas usage function (yearly integral ~ 1) and user data
    yearly_usage_guesses = []
    for i in range(1, len(usage_data)):
        start_entry = usage_data[i-1]
        end_entry = usage_data[i]
        
        # integral of gas usage function over the period
        integral = integral_between_days(gas_usage_function, start_entry.day, end_entry.day)

        if integral == 0:
            raise ValueError(f"Integral is zero between days {start_entry.day} and {end_entry.day}. Input data should not contain more than one entry per date. Please check input data and gas_usage_function.")
        
        user_usage = end_entry.usage - start_entry.usage
        yearly_usage_guess = user_usage / (integral / yearly_integral)
        yearly_usage_guesses.append(yearly_usage_guess)


    yearly_usage_best_fit = sum(yearly_usage_guesses) / len(yearly_usage_guesses)
    standard_deviation = (sum((x - yearly_usage_best_fit) ** 2 for x in yearly_usage_guesses) / len(yearly_usage_guesses)) ** 0.5
    print(f"Fitted average gas usage (unit depends on input data): {yearly_usage_best_fit:.0f} ± {standard_deviation:.0f}")

 
    plt.figure()
    plt.plot(yearly_usage_guesses, marker='o', linestyle='-', label='Yearly Gas Usage Guesses')
    plt.axhline(y=yearly_usage_best_fit, color='r', linestyle='--', label='Best Fit Yearly Usage')
    plt.xlabel('Index')
    plt.ylabel('Yearly Usage (m³ or kWh)')
    plt.xticks(range(len(yearly_usage_guesses)))
    plt.title('Gas Usage Fit')
    plt.legend()
    plt.show()