import random
from typing import List, Dict
from datetime import datetime, timedelta
from tqdm import tqdm
from src.utils.rate_limiter import RateLimiter


class PaymentGenerator:
    def __init__(self, config: Dict, invoices: List[Dict]):
        self.config = config
        self.invoices = invoices
        self.rate_limiter = RateLimiter(config['general']['max_operations_per_second'])

    def generate_payments(self) -> List[Dict]:
        payments = []
        for invoice in tqdm(self.invoices, desc="Generating Payments"):
            self.rate_limiter.limit()
            if invoice['status'] in ['Approved', 'Paid']:
                payment = self._generate_single_payment(invoice)
                payments.append(payment)
        return payments

    def _generate_single_payment(self, invoice: Dict) -> Dict:
        payment_date = self._generate_payment_date(invoice)
        payment_amount = self._calculate_payment_amount(invoice, payment_date)

        payment = {
            "payment_id": f"PAY{random.randint(1000000, 9999999)}",
            "invoice_number": invoice['invoice_number'],
            "po_number": invoice['po_number'],
            "vendor_id": invoice['vendor_id'],
            "vendor_name": invoice['vendor_name'],
            "payment_date": payment_date.strftime("%Y-%m-%d"),
            "amount": payment_amount,
            "currency": invoice['currency'],
            "payment_method": self._select_payment_method(),
            "status": "Completed" if payment_amount == invoice['total_amount'] else "Partial",
            "notes": self._generate_payment_notes(invoice, payment_date, payment_amount)
        }

        return payment

    def _generate_payment_date(self, invoice: Dict) -> datetime:
        invoice_date = datetime.strptime(invoice['invoice_date'], "%Y-%m-%d")
        due_date = datetime.strptime(invoice['due_date'], "%Y-%m-%d")

        # Simulate early, on-time, and late payments
        payment_scenario = random.choices(['early', 'on-time', 'late'], weights=[0.2, 0.6, 0.2])[0]

        if payment_scenario == 'early':
            return invoice_date + timedelta(days=random.randint(1, (due_date - invoice_date).days - 1))
        elif payment_scenario == 'on-time':
            return due_date
        else:  # late payment
            return due_date + timedelta(days=random.randint(1, 30))  # Assume max 30 days late

    def _calculate_payment_amount(self, invoice: Dict, payment_date: datetime) -> float:
        invoice_date = datetime.strptime(invoice['invoice_date'], "%Y-%m-%d")
        due_date = datetime.strptime(invoice['due_date'], "%Y-%m-%d")

        # Apply early payment discount if applicable
        if "2% 10" in invoice['payment_terms'] and (payment_date - invoice_date).days <= 10:
            discounted_amount = round(invoice['total_amount'] * 0.98, 2)
        else:
            discounted_amount = invoice['total_amount']

        # Simulate partial payments
        if random.random() < 0.1:  # 10% chance of partial payment
            return round(discounted_amount * random.uniform(0.5, 0.99), 2)
        else:
            return discounted_amount

    def _select_payment_method(self) -> str:
        return random.choice(self.config['payments']['methods'])

    def _generate_payment_notes(self, invoice: Dict, payment_date: datetime, payment_amount: float) -> str:
        notes = []

        invoice_date = datetime.strptime(invoice['invoice_date'], "%Y-%m-%d")
        due_date = datetime.strptime(invoice['due_date'], "%Y-%m-%d")

        if payment_date < due_date:
            notes.append("Early payment")
            if "2% 10" in invoice['payment_terms'] and (payment_date - invoice_date).days <= 10:
                notes.append("2% discount applied")
        elif payment_date > due_date:
            notes.append("Late payment")

        if payment_amount < invoice['total_amount']:
            notes.append("Partial payment")
            notes.append(f"Remaining balance: {invoice['total_amount'] - payment_amount:.2f} {invoice['currency']}")

        if not notes:
            notes.append("Payment processed as per terms")

        return "; ".join(notes)


def generate_payments(config: Dict, invoices: List[Dict]) -> List[Dict]:
    generator = PaymentGenerator(config, invoices)
    return generator.generate_payments()