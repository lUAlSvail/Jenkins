import pickle


class User:
    def __init__(self):
        self.login = "213123"
        self.password = "dasdasd"
        self.age = {"old": 30}



new_user = User()
pickle_it = open("User.pickle", "wb")
pickle.dump(new_user, pickle_it)
pickle_it.close()

pickle_back = open("User.pickle", "rb")

get_user = pickle.load(pickle_back)

print(get_user.__dict__)





import pickle
import selenium.webdriver

driver = selenium.webdriver.Firefox()
driver.get("http://www.google.com")
pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

driver = selenium.webdriver.Firefox()
driver.get("http://www.autodoc.de")
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)