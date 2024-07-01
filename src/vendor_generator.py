import random
from typing import List, Dict
from faker import Faker
from tqdm import tqdm
from src.description_generator import DescriptionGenerator
from src.utils.rate_limiter import RateLimiter

fake = Faker()


class VendorGenerator:
    def __init__(self, config: Dict, description_generator: DescriptionGenerator):
        self.config = config
        self.description_generator = description_generator
        self.rate_limiter = RateLimiter(config['general']['max_operations_per_second'])

    def generate_vendors(self) -> List[Dict]:
        total_vendors = self.config['vendors']['total_count']
        vendors = []

        for _ in tqdm(range(total_vendors), desc="Generating Vendors"):
            self.rate_limiter.limit()
            vendor = self._generate_single_vendor()
            vendors.append(vendor)

        return vendors

    def _generate_single_vendor(self) -> Dict:
        vendor_id = f"V{fake.unique.random_number(digits=7)}"
        name = fake.company()
        regions = self._assign_regions()
        specializations = random.sample(self.config['items']['categories'], random.randint(1, 3))

        vendor = {
            "vendor_id": vendor_id,
            "name": name,
            "description": self.description_generator.generate_description("Professional Services"),
            "address": fake.address(),
            "tax_id": fake.ssn(),  # This is a simplification; in reality, tax IDs would vary by country
            "payment_terms": random.choice(self.config['vendors']['payment_terms']),
            "regions": regions,
            "specializations": specializations,
            "rating": round(random.uniform(1, 5), 1),
            "is_preferred": random.random() < 0.2,  # 20% chance of being a preferred vendor
            "contact": {
                "name": fake.name(),
                "email": fake.email(),
                "phone": fake.phone_number()
            }
        }

        return vendor

    def _assign_regions(self) -> List[str]:
        all_regions = [region['name'] for region in self.config['regions']]
        distribution = self.config['vendors']['allowed_regions_distribution']

        if random.random() < distribution['single_region']:
            return [random.choice(all_regions)]
        else:
            num_regions = random.randint(2, len(all_regions))
            return random.sample(all_regions, num_regions)


def generate_vendors(config: Dict, description_generator: DescriptionGenerator) -> List[Dict]:
    generator = VendorGenerator(config, description_generator)
    return generator.generate_vendors()