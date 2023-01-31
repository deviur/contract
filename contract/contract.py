import os
import math
import weasyprint
from typing import Dict
from datetime import datetime, timedelta
from string import Template
from num_to_rus import Converter
from .exceptions import ContractValuesError
from contract.config import *

conv = Converter()


class Contract:
    def __init__(self, required_values: Dict, template_file: str = None):

        if not template_file:
            template_file = 'template.html'

        if not all(value in REQUIRED_VALUES for value in required_values):
            raise ContractValuesError('Не указано требуемое значение')
            return

        self._contract_data = _create_contract_values(required_values)
        self._html_string = self._load_template(template_file)

    def write_pdf(self, filename: str):
        pdf = weasyprint.HTML(string=self._html_string)
        pdf.write_pdf(filename)

    def _load_template(self, filename: str):
        with open(filename, 'r') as f:
            template = Template(f.read())
        return template.safe_substitute(self._contract_data)


def _create_contract_values(required_values):
    today = datetime.today()
    d1 = datetime.strptime(required_values['arrival_date'], '%d.%m.%Y')
    d2 = datetime.strptime(required_values['eviction_date'], '%d.%m.%Y')
    d2 = d1 + timedelta(days=1) if d2 <= d1 else d2
    contract_date = today if today <= d1 else d1
    delta = (d2 - d1).days
    guests_number = int(required_values['guests_number'])
    total_fee = round(float(required_values['total_fee']))
    daily_fee = math.ceil(total_fee / delta)
    deposit = round(float(required_values['deposit']))
    contract_data = {}
    contract_data.update(required_values)
    contract_data['contract_date'] = contract_date.strftime('%d.%m.%Y')
    contract_data['contract_number'] = contract_date.strftime('%y%m%d%H%M')
    contract_data['days_number'] = str(delta)
    contract_data['days_number_in_words'] = conv.convert(delta)
    contract_data['apartment_area'] = APARTMENTS[required_values['apartment_id']][0]
    contract_data['apartment_address'] = APARTMENTS[required_values['apartment_id']][1]
    contract_data['guests_number_in_words'] = conv.convert(guests_number)
    contract_data['daily_fee'] = str(daily_fee)
    contract_data['daily_fee_in_words'] = conv.convert(daily_fee)
    contract_data['total_fee_in_words'] = conv.convert(total_fee)
    contract_data['deposit_in_words'] = conv.convert(deposit)
    return contract_data
