# Required Packages
from Resource import htmlmin
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Managers import lgbtManager

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Baker McKenzie"
        self.ownerUsername = "bakermckenzie"
        self.scrapPageURL = "https://www.bakermckenzie.com/en/careers/job-opportunities/?locations=4080cf4b-d685-4ddb-bb31-d94ecb1cc11a&skip=1000000&scroll=100000"
        self.feedType = self.feedTypeWebScrap
        self.jobTrackingVariable = "ext_source=LGBTJobs"

        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL, True)
        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".opportunity-grid"))
        )

    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()

        try:

            jobContainers = self.chrome.find_elements_by_css_selector(".opportunity-grid .opportunity-item")
            for jobContainer in jobContainers:

                title = jobContainer.find_element_by_css_selector(".opportunity-link").text.replace("\"","\'")
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector(
                    ".opportunity-link").get_attribute('href')
                self.job.setLink(link)

                location = jobContainer.find_element_by_css_selector(".opportunity-header span[data-bind='text: Location']").text
                self.job.setLocation(location)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                link = self.chrome.find_element_by_css_selector(".main-column .header-text-module .apply-prompt a").get_attribute('href')
                self.jobs[currentJobIndex].setLink(link, self.jobTrackingVariable, lgbtManager.site.LGBT)
                self.jobs[currentJobIndex].setLink(link, self.jobTrackingVariable, lgbtManager.site.BME)
                self.jobs[currentJobIndex].setLink(link, self.jobTrackingVariable, lgbtManager.site.DISABILITY)

                description = self.chrome.find_element_by_css_selector(".main-column > .header-text-module:nth-child(1) .text-copy").get_attribute('innerHTML')

                self.jobs[currentJobIndex].setDescription(description)



            return True

        except:
            self.exceptionLogging()
            return False

