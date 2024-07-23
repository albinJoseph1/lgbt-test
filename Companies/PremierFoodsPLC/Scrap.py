# Required Packages
import time
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
        self.companyName = "Premier Foods PLC"
        self.ownerUsername = "premierfoodsplc"
        self.scrapPageURL = "https://careers.premierfoods.co.uk/search/?createNewAlert=false&q=&locationsearch=United+Kingdom"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#job-tile-list .job-tile"))
        )

    def loadJobs(self):
        self.loadScrapPage()

        try:
            jobContainers = self.chrome.find_elements_by_css_selector("#job-tile-list .job-tile")
            for jobContainer in jobContainers:

                link = jobContainer.find_element_by_css_selector(".job .jobTitle-link").get_attribute('href')
                self.job.setLink(link)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                title = self.chrome.find_element_by_css_selector(".jobDisplayShell #job-title").text
                self.jobs[currentJobIndex].setTitle(title)

                location = self.chrome.find_element_by_css_selector(".jobDisplayShell .jobGeoLocation").text
                self.jobs[currentJobIndex].setLocation(location)

                description = self.chrome.find_element_by_css_selector(".jobdescription").get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)


            return True

        except:
            self.exceptionLogging()
            return False