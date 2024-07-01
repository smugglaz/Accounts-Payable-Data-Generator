import random
from typing import List, Dict
from datetime import datetime, timedelta
from tqdm import tqdm
from src.utils.rate_limiter import RateLimiter


class InvoiceGenerator:
    def __init__(self, config: Dict, purchase_orders: List[Dict]):
        self.config = config
        self.purchase_orders = purchase_orders
        self.rate_limiter = RateLimiter(config['general']['max_operations_per_second'])

    def generate_invoices(self) -> List[Dict]:
        invoices = []
        for po in tqdm(self.purchase_orders, desc="Generating Invoices"):
            self.rate_limiter.limit()
            invoice_count = self._determine_invoice_count(po)
            for _ in range(invoice_count):
                invoice = self._generate_single_invoice(po)
                invoices.append(invoice)
        return invoices

    def _determine_invoice_count(self, po: Dict) -> int:
        # Simulate scenarios where a PO might have multiple invoices
        return random.choices([1, 2, 3], weights=[0.8, 0.15, 0.05])[0]

    def _generate_single_invoice(self, po: Dict) -> Dict:
        invoice_date = self._generate_invoice_date(po['po_date'])
        items = self._generate_invoice_items(po['items'])
        subtotal = sum(item['total_price'] for item in items)
        tax_amount = sum(item['tax_amount'] for item in items)
        total_amount = subtotal + tax_amount

        invoice = {
            "invoice_number": f"INV{random.randint(1000000, 9999999)}",
            "po_number": po['po_number'],
            "vendor_id": po['vendor_id'],
            "vendor_name": po['vendor_name'],
            "invoice_date": invoice_date.strftime("%Y-%m-%d"),
            "due_date": self._calculate_due_date(invoice_date, po['terms_and_conditions']),
            "currency": po['currency'],
            "items": items,
            "subtotal": subtotal,
            "tax_amount": tax_amount,
            "total_amount": total_amount,
            "status": self._determine_invoice_status(),
            "payment_terms": po['terms_and_conditions'],
            "notes": self._generate_invoice_notes()
        }

        if invoice['status'] == 'Blocked':
            invoice['block_reason'] = random.choice(self.config['invoices']['block_reasons'])

        # Simulate GRIR issues
        if random.random() < self.config['invoices']['grir_probability']:
            invoice['grir_issue'] = self._generate_grir_issue()

        return invoice

    def _generate_invoice_date(self, po_date: str) -> datetime:
        po_date = datetime.strptime(po_date, "%Y-%m-%d")
        max_days = 30  # Assume invoice is created within 30 days of PO
        return po_date + timedelta(days=random.randint(1, max_days))

    def _calculate_due_date(self, invoice_date: datetime, payment_terms: str) -> str:
        # Extract the number of days from payment terms
        terms_parts = payment_terms.split()
        if len(terms_parts) >= 2 and terms_parts[-1].isdigit():
            terms_days = int(terms_parts[-1])
        elif "2% 10 Net 30" in payment_terms:
            terms_days = 30
        else:
            # Default to 30 days if unable to parse
            terms_days = 30

        return (invoice_date + timedelta(days=terms_days)).strftime("%Y-%m-%d")

    def _generate_invoice_items(self, po_items: List[Dict]) -> List[Dict]:
        invoice_items = []
        for item in po_items:
            if random.random() < 0.95:  # 95% chance to include each PO item
                invoice_item = item.copy()

                # Simulate price discrepancies
                if random.random() < 0.1:  # 10% chance of price discrepancy
                    invoice_item['unit_price'] = round(item['unit_price'] * random.uniform(0.95, 1.05), 2)

                # Simulate quantity discrepancies
                if random.random() < 0.05:  # 5% chance of quantity discrepancy
                    invoice_item['quantity'] = max(1, item['quantity'] + random.choice([-1, 1]))

                invoice_item['total_price'] = invoice_item['quantity'] * invoice_item['unit_price']
                invoice_item['tax_amount'] = invoice_item['total_price'] * invoice_item['tax_rate']

                invoice_items.append(invoice_item)

        return invoice_items

    def _determine_invoice_status(self) -> str:
        return random.choices(
            self.config['invoices']['statuses'],
            weights=[0.2, 0.6, 0.15, 0.05],  # Adjust these weights as needed
            k=1
        )[0]

    def _generate_invoice_notes(self) -> str:
        notes = [
            "Please process for payment",
            "Discount applied as per contract",
            "Partial delivery - more to follow",
            "Rush processing requested",
            "Credit memo to follow for previous overcharge"
        ]
        return random.choice(notes)

    def _generate_grir_issue(self) -> Dict:
        issues = [
            {"type": "Quantity Mismatch", "description": "Invoice quantity doesn't match goods received"},
            {"type": "Price Mismatch", "description": "Unit price on invoice differs from PO price"},
            {"type": "Missing Goods Receipt", "description": "No record of goods receipt in the system"},
            {"type": "Delivery Date Mismatch", "description": "Invoice date is earlier than the delivery date"},
        ]
        return random.choice(issues)


def generate_invoices(config: Dict, purchase_orders: List[Dict]) -> List[Dict]:
    generator = InvoiceGenerator(config, purchase_orders)
    return generator.generate_invoices()