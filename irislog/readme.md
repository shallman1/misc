# IrisLog: Synthetic Log Injection Script

## Description

IrisLog is a synthetic log injection tool designed for use with the DomainTools integration demo environment. This tool 
dynamically generates logs using the latest domain and IP data retrieved from the DomainTools Iris Investigate API. Utilizing 
a search hash, IrisLog pulls information about domains that were first seen within the last hour and have a risk score of 99, 
ensuring that the logs reflect current high-risk entities, the search hash can also be replaced and the script will 
dynamically pull the first page of results. IrisLog is built with scalability in mind, allowing for the easy addition of new
log templates and SIEM configurations as needed.

## Features

- *Dynamic Log Generation*: Create logs with up-to-date threat data from DomainTools.
- *High-Risk Domain Focus*: Targets domains with the highest risk scores for timely and relevant log information.
- *Scalability*: Designed to easily incorporate more log templates and expand to additional SIEM systems.
- *SIEM Integration*: Comes pre-configured with a Splunk integration and can be extended to other SIEM platforms.
- *Customizable Templates*: Includes a variety of log templates that can be tailored to specific use cases.


## Usage
To use IrisLog, perform the following steps:
1. Update `IrisLog.py` with your DomainTools API credentials and desired search hash.
2. Configure the SIEM endpoint details in the script.
3. Run the script using Python with the command `python irisLog.py`.
4. The script will fetch domain data from DomainTools and inject synthetic logs into the configured SIEM system.


## Adding Log Templates
To add new log templates:
1. Define a new class in `log_templates.py` that inherits from `LogTemplate`.
2. Add your log template strings to the `LOG_TEMPLATES` list within your class.

## Adding SIEM Configurations
To add support for additional SIEM systems:
1. Add a new configuration dictionary to the `SIEM_CONFIGS` object in `IrisLog.py`.
2. Include endpoint details, authentication headers, and any other necessary configuration parameters, also pipelines
may need to be incorporated depending on the SIEM, such as Elastic.
