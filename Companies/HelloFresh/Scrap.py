# Required Packages
from Resource import htmlmin
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
        self.companyName = "Hello Fresh"
        self.ownerUsername = "hellofresh"
        self.scrapPageURL = "https://careers.hellofresh.com/global/en/search-results?qcountry=United%20Kingdom"
        self.feedType = self.feedTypeWebScrap
        self.jobIndicesToRemove = []
        self.jobKey = 'title'
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-ph-at-id='jobs-list'] .jobs-list-item"))
        )

    def nextPage(self):

        has_next_page = bool( self.chrome.find_element_by_css_selector('.pagination > li:last-child > a').get_attribute('class') != 'au-target aurelia-hide')
        if has_next_page:
            next_page = self.chrome.find_element_by_css_selector('.pagination > li:last-child > a')
            self.chrome.clickElement(next_page)

            self.chrome.pageWait()

            WebDriverWait(self.chrome, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-ph-at-id='jobs-list'] .jobs-list-item"))
            )
            return has_next_page

        else:
            return False

    def loadJobs(self):
        self.loadScrapPage()

        try:
            while True:
                jobContainers = self.chrome.find_elements_by_css_selector(".jobs-list-item")
                for jobContainer in jobContainers:
                    title = jobContainer.find_element_by_css_selector('.job-title').text
                    title = title.strip()
                    self.job.setTitle(title)

                    link = jobContainer.find_element_by_css_selector('[ph-tevent="job_click"]').get_attribute('href')
                    self.job.setLink(link)

                    location = jobContainer.find_element_by_css_selector('.job-location').text
                    self.job.setLocation(location)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

                if self.nextPage():
                    pass
                else:
                    break

            jobIndex = 0
            for job in self.jobs:
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                isJobExists = bool(self.chrome.find_elements_by_css_selector(".job-description"))
                if isJobExists:
                    description = self.chrome.find_element_by_css_selector(".job-description .jd-info").get_attribute("innerHTML")
                    self.jobs[jobIndex].setDescription(description)
                    
                    jobIndex = jobIndex + 1
                else:
                    del self.jobs[jobIndex]

            return True
        except:
            self.exceptionLogging()
            return False

