from user_input import get_parsed_usage_data, GasUsageEntry
from fit_data import get_historic_data
from gas_usage_functions import fit_gas_usage_function, cumulative_integral_between_days

from dataclasses import dataclass
import matplotlib.pyplot as plt

if __name__ == "__main__":
    #get user data
    usage_data = get_parsed_usage_data("example_usage_data.txt")
    
    # get gas usage function
    gas_usage_function = fit_gas_usage_function(get_historic_data(2024))
    yearly_integral = cumulative_integral_between_days(gas_usage_function, 0, 365)

    # for each pair of consecutive entries, calculate the scaling factor between gas usage function (yearly integral ~ 1) and user data
    scaling_factors = []
    for i in range(1, len(usage_data)):
        start_entry = usage_data[i-1]
        end_entry = usage_data[i]
        
        # integral of gas usage function over the period
        integral = cumulative_integral_between_days(gas_usage_function, start_entry.day, end_entry.day)

        if integral == 0:
            raise ValueError(f"Integral is zero between days {start_entry.day} and {end_entry.day}. Input data should not contain more than one entry per date. Please check input data and gas_usage_function.")
        
        user_usage = end_entry.usage - start_entry.usage
        scaling_factor = user_usage / (integral / yearly_integral)
        scaling_factors.append(scaling_factor)


    average_scaling = sum(scaling_factors) / len(scaling_factors)
    standard_deviation = (sum((x - average_scaling) ** 2 for x in scaling_factors) / len(scaling_factors)) ** 0.5
    print(f"Fitted average gas usage (unit depends on input data): {average_scaling:.0f} ± {standard_deviation:.0f}")

 
    plt.figure()
    plt.plot(scaling_factors, marker='o', linestyle='-', label='Scaling Factors')
    plt.axhline(y=sum(scaling_factors)/len(scaling_factors), color='r', linestyle='--', label='Average Scaling Factor')
    plt.xlabel('Index')
    plt.ylabel('Scaling Factor (m³ or kWh)')
    plt.xticks(range(len(scaling_factors)))
    plt.title('Scaling Factors Between Consecutive Gas Usage Entries')
    plt.legend()
    plt.show()