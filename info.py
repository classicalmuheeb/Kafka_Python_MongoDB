from faker.providers import BaseProvider
from typing import OrderedDict, List

class BenefitsProvider(BaseProvider):
    """Custom Benefit Provider"""

    BENEFITS = [
        {'name': 'English classes', 'min_cost': 300, 'max_cost': 3000},
        {'name': 'Childcare benefits', 'min_cost': 100, 'max_cost': 800},
        {'name': 'Gym memberships or discounts', 'min_cost': 100, 'max_cost': 1500},
        {'name': 'Wellness programs', 'min_cost': 500, 'max_cost': 2000},
        {'name': 'Employee recognition programs', 'min_cost': 1000, 'max_cost': 2500},
        {'name': 'Relocation assistance', 'min_cost': 2500, 'max_cost': 4500},
        {'name': 'Commuting / travel assistance', 'min_cost': 100, 'max_cost': 500},
        {'name': 'Telecommuting options', 'min_cost': 15, 'max_cost': 300},
        {'name': 'Workplace perks', 'min_cost': 200, 'max_cost': 600},
        {'name': 'Paid training and development', 'min_cost': 2500, 'max_cost': 8000}
    ]

    def benefit(self):
        return self.random_element(self.BENEFITS)

    def all_benefits(self):
        return self.BENEFITS

class EthnicityProvider(BaseProvider):
    ETHNICS = OrderedDict([
        ("Asian", 0.7),
        ("Caucausian", 0.4),
        ("African American", 0.3),
        ("Latino", 0.5),
        ("African", 0.8),
        ("Armenian Americans", 0.2),
        ("Greek Americans", 0.5),
        ("Italian Americans", 0.2),
        ("Polish Americans", 0.4),
        ("Irish Americans", 0.20),
        ("German Americans", 0.3),
        ("Russian Americans", 0.2),
        ("Ukrainian Americans", 0.3)
    ])

    def ethnic(self) -> str:
        return self.random_elements(self.ETHNICS, length=1, use_weighting=True)
    
    def all_ethnicities(self) -> List[str]:
        return list(self.ETHNICS.keys())