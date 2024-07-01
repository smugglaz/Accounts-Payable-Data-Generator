import yaml
import logging
from pathlib import Path
from src.description_generator import DescriptionGenerator
from src.vendor_generator import generate_vendors
from src.po_generator import generate_purchase_orders
from src.invoice_generator import generate_invoices
from src.payment_generator import generate_payments
from src.utils.data_writer import write_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_config(config_path: str) -> dict:
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def main():
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    config = load_config(config_path)

    description_config_path = Path(__file__).parent.parent / "config" / "description_config.yaml"
    description_generator = DescriptionGenerator(description_config_path)

    logger.info("Starting AP data generation process")

    vendors = generate_vendors(config, description_generator)
    logger.info(f"Generated {len(vendors)} vendors")
    write_data(vendors, 'vendors', config['general']['output_format'])

    purchase_orders = generate_purchase_orders(config, vendors, description_generator)
    logger.info(f"Generated {len(purchase_orders)} purchase orders")
    write_data(purchase_orders, 'purchase_orders', config['general']['output_format'])

    invoices = generate_invoices(config, purchase_orders)
    logger.info(f"Generated {len(invoices)} invoices")
    write_data(invoices, 'invoices', config['general']['output_format'])

    payments = generate_payments(config, invoices)
    logger.info(f"Generated {len(payments)} payments")
    write_data(payments, 'payments', config['general']['output_format'])

    logger.info("AP data generation process completed")


if __name__ == "__main__":
    main()