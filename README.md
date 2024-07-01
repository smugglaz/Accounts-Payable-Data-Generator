# Accounts Payable Data Generator

## Project Overview

This project generates synthetic data for an Accounts Payable (AP) system of a Fortune 500 company. It simulates various aspects of the AP process, including vendors, purchase orders, invoices, and payments across multiple regions and currencies.

## Project Structure

```
ap_data_generator/
│
├── config/
│   ├── config.yaml
│   └── description_config.yaml
│
├── src/
│   ├── main.py
│   ├── description_generator.py
│   ├── vendor_generator.py
│   ├── po_generator.py
│   ├── invoice_generator.py
│   ├── payment_generator.py
│   └── utils/
│       ├── init.py
│       ├── data_writer.py
│       └── rate_limiter.py
│
├── requirements.txt
└── README.md
```

## Key Components

1. **Configuration Files**: 
   - `config.yaml`: Main configuration file for the data generation process.
   - `description_config.yaml`: Configuration for generating realistic item descriptions.

2. **Main Script** (`main.py`): 
   Orchestrates the entire data generation process.

3. **Generator Modules**:
   - `description_generator.py`: Generates realistic item descriptions.
   - `vendor_generator.py`: Creates vendor data.
   - `po_generator.py`: Generates purchase orders.
   - `invoice_generator.py`: Creates invoices based on purchase orders.
   - `payment_generator.py`: Generates payment data for invoices.

4. **Utility Modules**:
   - `data_writer.py`: Handles writing generated data to CSV or JSON files.
   - `rate_limiter.py`: Implements rate limiting to control data generation speed.

## Implementation Steps

1. **Setup**:
   - Create the project directory structure as shown above.
   - Install required dependencies: `pip install -r requirements.txt`

2. **Configuration**:
   - Set up `config.yaml` and `description_config.yaml` in the `config/` directory.
   - Adjust parameters like number of vendors, POs, date ranges, etc. in `config.yaml`.
   - Customize description templates and word lists in `description_config.yaml`.

3. **Implement Utility Modules**:
   - Create `rate_limiter.py` and `data_writer.py` in the `src/utils/` directory.

4. **Implement Generator Modules**:
   - Create each generator module (`description_generator.py`, `vendor_generator.py`, etc.) in the `src/` directory.
   - Each module should have a main generator class and a function to interface with `main.py`.

5. **Main Script**:
   - Implement `main.py` to orchestrate the data generation process.
   - Use the generator modules in sequence: vendors -> POs -> invoices -> payments.

6. **Testing and Refinement**:
   - Run the script and check the output data for realism and consistency.
   - Adjust configurations and generation logic as needed.

## Key Considerations

- **Rate Limiting**: Use the `RateLimiter` class to prevent overwhelming system resources.
- **Data Consistency**: Ensure relationships between entities (e.g., POs referencing valid vendors) are maintained.
- **Realistic Scenarios**: Implement various real-world scenarios like partial payments, early payment discounts, and GRIR issues.
- **Regional Variations**: Account for different currencies, tax rates, and regulations across regions.
- **Scalability**: The modular design allows for easy addition of new features or modification of existing ones.

## Running the Project

1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Configure `config.yaml` and `description_config.yaml` as needed.
3. Run the main script: `python src/main.py`
4. Check the generated output files (CSV or JSON, as specified in the config).

## Extending the Project

To add new features or modify existing ones:
1. Update the relevant configuration in `config.yaml` or `description_config.yaml`.
2. Modify or add new generator modules in the `src/` directory.
3. Update `main.py` to incorporate any new data generation steps.

## Code Snippets

Here's a simple example of the `RateLimiter` class used throughout the project:

```
import time

class RateLimiter:
    def __init__(self, max_per_second):
        self.max_per_second = max_per_second
        self.allowance = max_per_second
        self.last_check = time.time()

    def limit(self):
        current = time.time()
        time_passed = current - self.last_check
        self.last_check = current
        self.allowance += time_passed * self.max_per_second
        if self.allowance > self.max_per_second:
            self.allowance = self.max_per_second
        if self.allowance < 1.0:
            time.sleep((1.0 - self.allowance) / self.max_per_second)
        else:
            self.allowance -= 1.0
```

This class is used in each generator to ensure that data generation doesn't exceed a specified rate, which is crucial for managing system resources and simulating real-world API limitations.

## Conclusion
This Accounts Payable Data Generator provides a flexible and extensible framework for creating realistic AP data. By following the implementation steps and understanding the key components, developers can easily generate large volumes of synthetic data that reflect the complexities of a global Fortune 500 company's AP processes.