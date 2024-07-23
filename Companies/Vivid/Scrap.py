# Required Packages
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Vivid"
        self.ownerUsername = "vividhomes"
        self.scrapPageURL = "https://vividhomes.current-vacancies.com/RSSFeeds/Vacancies/VIVID?feedID=CB423654376A4770B4B895876E196B6D"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.TAG_NAME, "channel"))
        )

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector("item")
            for jobContainer in jobContainers:
                title = jobContainer.find_element_by_css_selector("vtitle").text
                self.job.setTitle(title)

                location = jobContainer.find_element_by_css_selector("vlocation").text
                self.job.setLocation(location)

                link = jobContainer.text.split("l="+location.replace(" ","+").replace("/","%2f"))[0]
                link = link+"l="+location.replace(" ","+").replace("/","%2f")
                self.job.setLink(link)

                expireDate = jobContainer.find_element_by_css_selector("vexpirydate").text
                expireDate = datetime.strptime(expireDate, "%d/%m/%Y %H:%M:%S").strftime('%Y-%m-%d')
                self.job.setExpireDate(expireDate)

                salary = jobContainer.find_element_by_css_selector("vsalary").text
                self.job.setSalary(salary)

                description = jobContainer.find_element_by_css_selector("vadverttext").get_attribute('innerHTML')
                self.job.setDescription(description)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            return True
        except:
            self.exceptionLogging()
            return False