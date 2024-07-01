import random
from typing import List, Dict
from datetime import datetime, timedelta
from tqdm import tqdm
from src.description_generator import DescriptionGenerator
from src.utils.rate_limiter import RateLimiter


class PurchaseOrderGenerator:
    def __init__(self, config: Dict, vendors: List[Dict], description_generator: DescriptionGenerator):
        self.config = config
        self.vendors = vendors
        self.description_generator = description_generator
        self.rate_limiter = RateLimiter(config['general']['max_operations_per_second'])
        self.start_date = datetime.strptime(config['general']['start_date'], "%Y-%m-%d")
        self.end_date = datetime.strptime(config['general']['end_date'], "%Y-%m-%d")

    def generate_purchase_orders(self) -> List[Dict]:
        total_pos = self.config['purchase_orders']['total_count']
        purchase_orders = []

        for _ in tqdm(range(total_pos), desc="Generating Purchase Orders"):
            self.rate_limiter.limit()
            po = self._generate_single_po()
            purchase_orders.append(po)

        return purchase_orders

    def _generate_single_po(self) -> Dict:
        vendor = random.choice(self.vendors)
        region = random.choice(vendor['regions'])
        po_date = self._random_date(self.start_date, self.end_date)
        region_config = next(r for r in self.config['regions'] if r['name'] == region)
        currency = random.choice(region_config['currencies'])

        po = {
            "po_number": f"PO{random.randint(1000000, 9999999)}",
            "vendor_id": vendor['vendor_id'],
            "vendor_name": vendor['name'],
            "region": region,
            "po_date": po_date.strftime("%Y-%m-%d"),
            "currency": currency,
            "items": self._generate_line_items(vendor['specializations'], region, currency),
            "status": "Open",
            "shipping_address": self._generate_address(region),
            "billing_address": self._generate_address(region),
            "terms_and_conditions": f"Net {vendor['payment_terms']}",
            "notes": self._generate_notes()
        }

        po["total_amount"] = sum(item['total_price'] for item in po['items'])
        return po

    def _generate_line_items(self, specializations: List[str], region: str, currency: str) -> List[Dict]:
        num_items = random.randint(self.config['purchase_orders']['min_items'],
                                   self.config['purchase_orders']['max_items'])
        items = []
        for _ in range(num_items):
            category = random.choice(specializations)
            item_desc = self.description_generator.generate_item_description(category)
            quantity = random.randint(1, 100)
            unit_price = self._generate_unit_price(category, currency)
            total_price = quantity * unit_price
            tax_rate = self._get_tax_rate(category, region)

            item = {
                "item_number": f"ITEM{random.randint(100000, 999999)}",
                "description": item_desc['description'],
                "category": category,
                "quantity": quantity,
                "unit_price": unit_price,
                "total_price": total_price,
                "currency": currency,
                "tax_rate": tax_rate,
                "tax_amount": total_price * tax_rate,
                "brand": item_desc['brand'],
                "model": item_desc['model']
            }
            items.append(item)
        return items

    def _generate_unit_price(self, category: str, currency: str) -> float:
        base_price = random.uniform(10, 1000)
        exchange_rate = self.config['exchange_rates']['rates'][currency]
        return round(base_price * exchange_rate, 2)

    def _get_tax_rate(self, category: str, region: str) -> float:
        region_config = next(r for r in self.config['regions'] if r['name'] == region)
        return region_config['tax_rates'].get(category, region_config['tax_rates']['default'])

    def _random_date(self, start: datetime, end: datetime) -> datetime:
        return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

    def _generate_address(self, region: str) -> str:
        region_config = next(r for r in self.config['regions'] if r['name'] == region)
        return f"123 Business St, Anytown, {random.choice(region_config['countries'])}"

    def _generate_notes(self) -> str:
        notes = [
            "Please deliver during business hours",
            "Fragile items included, handle with care",
            "Contact provided number before delivery",
            "Installation services required",
            "Rush order, please expedite"
        ]
        return random.choice(notes)


def generate_purchase_orders(config: Dict, vendors: List[Dict], description_generator: DescriptionGenerator) -> List[
    Dict]:
    generator = PurchaseOrderGenerator(config, vendors, description_generator)
    return generator.generate_purchase_orders()