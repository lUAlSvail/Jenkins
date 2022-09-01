from datetime import date, timedelta, time
from typing import List

import allure
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
        fake = Faker("en_EN")
        self.uuid = None
        self.first_name = fake.first_name() + helpers.generate_digits(4)
        self.last_name = fake.last_name()
        self.gender = "F"
        self.phone = "+331{}".format(helpers.generate_digits(8))
        self.phone_without_code = self.phone.replace('+33', '')
        self.email = helpers.generate_email()
        self.password = "324234234"
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
        self.candidate.address.get_one_string_address()
        return self


def set_birthday(self, birthday: date) -> "CandidateBuilder":
    self.candidate.birthday = birthday
    return self


def set_is_news_mailing_enabled(self,
                                is_enabled: bool) -> "CandidateBuilder":
    self.candidate.is_news_mailing_enabled = is_enabled
    return self


def set_is_terms_accepted(self,
                          is_terms_accepted: bool) -> "CandidateBuilder":
    self.candidate.is_terms_accepted = is_terms_accepted
    return self


def set_uuid(self, uuid: str) -> "CandidateBuilder":
    self.candidate.uuid = uuid
    return self


def set_has_vehicle(self, has_vehicle: bool) -> "CandidateBuilder":
    self.candidate.has_vehicle = has_vehicle
    return self


def set_desired_job(self, job: Job) -> "CandidateBuilder":
    self.candidate.desired_job = job
    return self


def build(self) -> Candidate:
    assert self.candidate.has_contract_type_selected(), "Need to select contract type before build"
    return self.candidate





#decorator

def verify_request_status(func):
    """ This decorator check that response with specific trace id has been
        successfully processed by algolia """
    def wrapper_verify_request_status(*args, **kwargs):
        with allure.step("Wait until trace id processed by Algolia"):
            response_id = func(*args, **kwargs)
            counter = 0
            while counter < 100:
                response = get_request_algolia_status((response_id.headers._store['x-trace-id'][1]).split(',')[0])
                response_list = response.json()
                counter += 1
                for response in response_list:
                    if response['status'] != 'import_success':
                        time.sleep(0.5)
                        continue
                return response_id
            raise Exception('Response was not handled by algolia' + get_request_response(response_id))
    return wrapper_verify_request_status


#Factory
import os
from abc import ABC, abstractmethod
from appium import webdriver as appium_webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as OptionsChrome
from selenium.webdriver.chrome.service import Service as ServiceChrome
from webdriver_manager.chrome import ChromeDriverManager
from environment import (bs_username, bs_access_key, bs_app_id, device, job_name,
                         build_number, bs_remote_url)

class DriverWeb(ABC):
    """Class for browser drivers"""
    @staticmethod
    @abstractmethod
    def get_driver(executor, headless, mobile_emulation):
        """Return driver with given options"""
class DriverMobile(ABC):
    """Class for browser drivers"""
    @staticmethod
    @abstractmethod
    def get_driver(executor):
        """Return driver with given options"""
class DriverChrome(DriverWeb):
    """Class for creating Google Chrome driver"""
    @staticmethod
    def get_driver(executor="remote", headless: bool = False, mobile_emulation: bool = False):
        """Return driver with given options"""
        assert executor in {"remote", "local"}
        # Set options
        options = OptionsChrome()
        downloads_dir = os.path.abspath('downloads')
        if headless:
            options.headless = True
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1280')
        options.add_experimental_option("prefs", {
            "download.default_directory": downloads_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
        })
        if mobile_emulation:
            mobile_emulation = {"deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0}}
            options.add_experimental_option("mobileEmulation", mobile_emulation)
        options.set_capability("goog:loggingPrefs", {'browser': 'ALL', 'driver': 'ALL', 'client': 'ALL', 'performance': 'ALL'})
        # Set executor
        if executor == "remote":
            return webdriver.Remote(command_executor='http://selenium-hub:4444', options=options)
        else:
            executor_url = ChromeDriverManager().install()
            service = ServiceChrome(executor_url)
            return webdriver.Chrome(service=service, options=options)
class DriverAndroid(DriverMobile):
    """Class for Android driver creation"""
    @staticmethod
    def get_driver(executor="remote"):
        """Return android driver"""
        assert executor in {"browserstack", "local"}
        DEVICE_POOL = {
            'Samsung Galaxy S21': '11.0', 'Google Nexus 6': '6.0', 'Samsung Galaxy Tab S7': '10.0'
        }
        if executor == "browserstack":
            desired_caps = {
                "browserstack.user": bs_username,
                "browserstack.key": bs_access_key,
                "language": "fr",
                "locale": "FR",
                "automationName": "UiAutomator2",
                "app": bs_app_id,
                "device": device,
                "os_version": DEVICE_POOL[device],  # get from dictionary mapped to device
                "project": "Troops QA mobile",
                "build": f"{job_name} {build_number}",
                "autoGrantPermissions": True,
                "browserstack.appium_version": "1.22.0",
                # Make appium wait up to 5 min for command
                # (sometimes our tests make API calls and don't communicate with Appium)
                # by default Appium shut off session after 60 sec of inactivity
                "newCommandTimeout": 600,
                "browserstack.networkLogs": "true",
                "ignoreUnimportantViews": True,
                "name": SharedStorage().get_value('test_title')  # title of a test
            }
        else:
            desired_caps = {
                "appium:app": "/home/vlad/Downloads/6.3.102/6.3.102_qa.apk",  # Awful hardcode for now :)
                "platformName": "Android",
                "appium:platformVersion": "10",
                "appium:deviceName": "1c891718920c7ece",
                "autoGrantPermissions": True,
                "automationName": "UiAutomator2",
                # Make appium wait up to 5 min for command
                # (sometimes our tests make API calls and don't communicate with Appium)
                # by default Appium shut off session after 60 sec of inactivity
                "newCommandTimeout": 600
            }
        url = bs_remote_url if executor == "browserstack" else "http://127.0.0.1:1234/wd/hub"
        return appium_webdriver.Remote(command_executor=url, desired_capabilities=desired_caps)
class DriveriOS(DriverMobile):
    """Class for iOS driver creation"""
    @staticmethod
    def get_driver(executor="remote"):
        """Return iOS driver"""
        assert executor in {"browserstack", "local"}
        DEVICE_POOL = {
            'iPhone 7': '10',
            'iPhone 12': '14',
            'iPad Air 2019': '13',
            'iPhone 13': '15'
        }
        if executor == "browserstack":
            desired_caps = {
                "browserstack.user": bs_username,
                "browserstack.key": bs_access_key,
                "language": "fr",
                "locale": "FR",
                "app": bs_app_id,
                "device": device,
                "os_version": DEVICE_POOL[device],  # get from dictionary mapped to device
                "project": "QA mobile",
                "build": f"{job_name} {build_number}",
                "browserstack.appium_version": "1.22.0",
                # Make appium wait up to 5 min for command
                # (sometimes our tests make API calls and don't communicate with Appium)
                # by default Appium shut off session after 60 sec of inactivity
                "newCommandTimeout": 600,
                "autoAcceptAlerts": True,
                "name": SharedStorage().get_value('test_title')
            }
        else:
            raise NotImplementedError("Local running is not implemented")
        url = bs_remote_url if executor == "browserstack" else "http://127.0.0.1:1234/wd/hub"
        return appium_webdriver.Remote(command_executor=url, desired_capabilities=desired_caps)


class AddressFactory(ABC):
    """
    Address factory for creating Address objects
    """
    @abstractmethod
    def get_address(self) -> Address:
        """Return address"""
class RandomStringAddress(AddressFactory):
    def get_address(self) -> Address:
        """
        Return address in format 'France <random 3 digits>
        """
        address = 'France, ' + helpers.generate_digits(3)
        return Address(country=address)
    
class ValidAddress(AddressFactory):
    """
    This class produce address that can be found via Google API
    """
    def get_address(self) -> Address:
        common_data = test_data.get_common_data()
        return Address(
            country="France", city="Ballots", street="Rue Sainte-Anne",
            house_number="7", postal_code="53350", lat=47.89894876802425, long=-1.0490504209648162,
            country_id=common_data['country_id']
        )
    def get_another_address(self) -> Address:
        common_data = test_data.get_common_data()
        return Address(country="France", city="Paris", street="Boulevard Vincent Auriol", house_number="22",
                       postal_code="75013", lat=48.83656680000001, long=2.3714388,
                       country_id=common_data['country_id'])
class AnotherValidAddress(AddressFactory):
    """
    This class produce address that can be found via Google API
    In some tests you need 2 valid addresses to be different
    """
    def get_address(self) -> Address:
        common_data = test_data.get_common_data()
        return Address(country="France", city="Fréjus", street="Rue Jean Giono", house_number="261",
                       postal_code="83600", lat=43.435356420521316, long=6.75712323896745,
                       country_id=common_data['country_id'])
class AnotherValidAddressWithPrecision(AddressFactory):
    def get_address(self) -> Address:
        common_data = test_data.get_common_data()
        return Address(country="France",
                       city="Orléans",
                       street="Rue de Saint-Denis",
                       house_number="722",
                       postal_code="45560",
                       lat=47.880222,
                       long=1.946972,
                       country_id=common_data['country_id'],
                       is_manual=False,
                       precision="Turn left behind the main building")
class AddressForPiTest(AddressFactory):
    """
    This is valid address used for PI testing
    """
    def get_address(self) -> Address:
        return Address(
            country="France",
            city="Paris",
            street="Rue du Faubourg Saint-Antoine",
            house_number="133",
            postal_code="75012",
            lat=48.8510418,
            long=2.3777799,
            country_id="6abab572-4181-469f-b286-a34752e4df42"
        )
class ValidCustomAddress(AddressFactory):
    """
    This address has valid country and city so should work
    But it has invalid street (or street that exist in real life, but Google API doesn't aware about it)
    This is for testing "custom address" feature, it can't be found by Google API
    """
    def get_address(self) -> Address:
        return Address(country="France", city="Ballots", street="Rue-Sainte-Vlade", house_number="122", postal_code="53350")




# MEMO patern

"""Memento class for saving the data"""


class Memento:
    """Constructor function"""

    def __init__(self, file, content):
        """put all your file content here"""

        self.file = file
        self.content = content


"""It's a File Writing Utility"""


class FileWriterUtility:
    """Constructor Function"""

    def __init__(self, file):
        """store the input file data"""
        self.file = file
        self.content = ""

    """Write the data into the file"""

    def write(self, string):
        self.content += string

    """save the data into the Memento"""

    def save(self):
        return Memento(self.file, self.content)

    """UNDO feature provided"""

    def undo(self, memento):
        self.file = memento.file
        self.content = memento.content


"""CareTaker for FileWriter"""


class FileWriterCaretaker:
    """saves the data"""

    def save(self, writer):
        self.obj = writer.save()

    """undo the content"""

    def undo(self, writer):
        writer.undo(self.obj)


if __name__ == '__main__':
    """create the caretaker object"""
    caretaker = FileWriterCaretaker()

    """create the writer object"""
    writer = FileWriterUtility("Test.txt")

    """write data into file using writer object"""
    writer.write("First vision of Test\n")
    print(writer.content + "\n\n")

    """save the file"""
    caretaker.save(writer)

    """again write using the writer """
    writer.write("Second vision of Test\n")

    print(writer.content + "\n\n")

    """undo the file"""
    caretaker.undo(writer)

    print(writer.content + "\n\n")
    print("hello")