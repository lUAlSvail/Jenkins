from datetime import date, timedelta
from typing import List
from faker import Faker
from constants.address_constants import Address, ValidAddress
from entities.job import Job
from entities import document
from environment import test_data
from utils import helpers


class Candidate:
    """Class representing candidate"""

    def __init__(self):
        common_data = test_data.get_common_data()
        fake = Faker("fr_FR")
        self.uuid = None
        self.first_name = fake.first_name() + helpers.generate_digits(4)
        self.last_name = fake.last_name()
        self.gender = "F"
        self.phone = "+331{}".format(helpers.generate_digits(8))
        self.phone_without_code = self.phone.replace('+33', '')
        self.email = helpers.generate_email()
        self.password = "11111111"
        self.address = ValidAddress().get_address()
        self.address_dict = self.address.get_dict_address_for_api()
        self.address_str = self.address.get_one_string_address()
        self.birthday = date.today() - timedelta(days=366 * 18)
        self.ssn_dob = f'{str(self.birthday.year)[-2:]}{self.birthday.strftime("%m")}'
        self.is_news_mailing_enabled = False
        self.is_terms_accepted = True
        self.contract_cdd = False
        self.contract_freelance = False
        self.contract_interim = False
        self.interim_tea_uuid = None
        self.has_vehicle = False
        self.token = None
        self.nationality = common_data['country_id']
        self.social_security: "document.SocialSecurityDocument" = None
        self.identity_justification: "document.IdentityDocument" = None
        self.work_agreements = []
        self.last_wa_uuid: str = None
        self.last_proposal_uuid: str = None
        self.maiden_name: str = None
        self.desired_job: Job = None

    def __repr__(self) -> str:
        return f"Candidate: {self.full_name} {self.email}"

    def __repr__(self) -> str:
        return f"Candidate: {self.full_name()} {self.email}"

    def full_name(self) -> str:
        """
        Return full name of candidate
        """
        return f'{self.first_name} {self.last_name}'

    def anonymized_name(self) -> str:
        """
        Return anonymized name of candidate
        """
        return f'{self.first_name} {self.last_name[0]}.'

    def has_contract_type_selected(self) -> List[str]:
        """
        Method show which contract types selected
        Return list of strings with contract type or empty list if no contract type selected
        """
        contract_types = []
        if self.contract_cdd:
            contract_types.append("cdd")
        if self.contract_freelance:
            contract_types.append("freelance")
        if self.contract_interim:
            contract_types.append("interim")
        return contract_types


class CandidateBuilder:
    """Builder for candidate class"""

    def __init__(self):
        self.candidate = Candidate()

    def set_name(self, name: str) -> "CandidateBuilder":
        self.candidate.first_name = name
        return self

    def set_last_name(self, last_name: str) -> "CandidateBuilder":
        self.candidate.last_name = last_name
        return self

    def set_gender(self, gender: str) -> "CandidateBuilder":
        assert gender in {"M", "F"}, f"Wrong gender argument: {gender}"
        self.candidate.gender = gender
        return self

    def set_phone(self, phone: str) -> "CandidateBuilder":
        self.candidate.phone = phone
        self.candidate.phone_without_code = phone.replace('+33', '')
        return self

    def set_email(self, email: str) -> "CandidateBuilder":
        self.candidate.email = email
        return self

    def set_password(self, password: str) -> "CandidateBuilder":
        self.candidate.password = password
        return self

    def set_address(self, address: Address) -> "CandidateBuilder":
        self.candidate.address = address
        self.candidate.address_dict = self.candidate.address.get_dict_address_for_api()
