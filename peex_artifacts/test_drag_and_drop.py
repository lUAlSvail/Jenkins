from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

def test_drag_and_drop():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get('http://www.dhtmlgoodies.com/scripts/drag-drop-custom/demo-drag-drop-3.html')
    drag = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[starts-with(@id, 'box') and text()='Rome']")))
    drop = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[starts-with(@id, 'box') and text()='South Korea']")))
    ActionChains(driver).drag_and_drop(drag, drop).perform()
    time.sleep(5)
    driver.quit()


def test_upload_file():
    def upload_file(self, file):
        path = get_upload_file_path(file)
        self.wait.wait_for_element(UPLOAD_FILE_LOCATOR).send_keys(path)
        self.action.click(SAVE_LOCATOR)

# functional keys
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_DOWN + 'j')

driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_DOWN + 'l')