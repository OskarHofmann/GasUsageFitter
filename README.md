# Gas Usage Fitter

Tool to estimate the yearly gas usage based on two or more intermediate meter readings

## Background 

I wanted to get an estimate of my yearly gas usage to compare contracts but did not have data of a full heating period at a new apartment yet. Available "gas usage calculators" just use the area of the apartment for a rough guess but I had data I wanted to use. So I wrote this tool.

## How it works

This tool first fits a function of gas usage per day to historic data and then fits that to two or more meter provided readings for a guess of your yearly usage. Two kinds of historic and standardized data for German households are provided. Note that this data averages all households and is therefore a mix of households that use gas for heating, warm water or both. That is the main reason for why there is still a non negligable gas usage in the summer in this data. Feel free to provide your own or better suited data. As the function to model the gas usage should be periodic over a year (assuming all years are on average equal regarding gas usage), I use a combination of sine and cosine functions with a period of 365 days. This function fits the historic data regarding cummulative usage per month quite well but has an unrealistic bump in the middle of the summer. If you find a better function to model yearly gas usage, feel free to contact me. :)

## How to use

The script works out of the box using example data when running main.py. To fit a function to model yearly gas usage, the function fit_gas_usage_function() must be provided with data for monthly gas usages (as this is the format typically available from data sources). Data for German households in 2024 and data based on German standards for heating usage calculations are available in the fit_data module. Modifying example_usage_data.txt (or providing another file to the get_parsed_usage_data() function) allows you to use your own meter readings. As long as there are at least two data points and there is only one data point per calendar day, there should be no further restrictions on how the data should look like. There is also no need to provide the data in order, as it will get sorted before use.
