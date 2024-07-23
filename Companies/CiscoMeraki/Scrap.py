# Required Packages
import time
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
        self.companyName = "Cisco Meraki"
        self.ownerUsername = "cisco"
        self.scrapPageURL = "https://meraki.cisco.com/jobs"
        self.feedType = self.feedTypeWebScrap
        self.locationFilters = ['London','Remote within UK']
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#open-positions"))
        )

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector("#open-positions .department li")
            for jobContainer in jobContainers:
                hasLocationFilter = False
                locationsOfJob = jobContainer.find_elements_by_css_selector("span.city")
                for locationFilter in self.locationFilters:
                    for locationOfJob in locationsOfJob:
                        if locationFilter in locationOfJob.text:
                            location = locationOfJob.text
                            hasLocationFilter = True
                            break

                if hasLocationFilter:
                    titleAnchor = jobContainer.find_element_by_css_selector("a")

                    title = titleAnchor.text
                    self.job.setTitle(title)

                    link = titleAnchor.get_attribute("href")
                    self.job.setLink(link)

                    self.chrome.clickElement(titleAnchor)

                    WebDriverWait(self.chrome, 100).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".job-description-container .job-description"))
                    )

                    description = self.chrome.find_element_by_css_selector(
                        ".job-description-container .job-description .encoded-job-description").get_attribute('innerHTML')
                    description = description.replace("&lt;", "<")
                    description = description.replace("&gt;", ">")

                    self.job.setDescription(description)

                    modalClose = self.chrome.find_element_by_css_selector(".close-modal img")
                    self.chrome.clickElement(modalClose)

                    self.job.setLocation(location)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

            return True
        except:
            self.exceptionLogging()
            return False