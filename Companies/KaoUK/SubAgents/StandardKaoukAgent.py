# Required Packages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Objects import Job

import time

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = ""
        self.ownerUsername = ""
        self.scrapPageURL = "https://jobs.kaocareers.com/jobs?limit=100&location=United%20Kingdom"
        self.feedType = self.feedTypeWebScrap
        self.moltonBrownJobs = []
        self.brandFilter = 'Molton Brown'
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".search-results__list"))
        )

    def nextPage(self):
        hasNextPage = bool(self.chrome.find_element_by_css_selector(".mat-paginator .mat-paginator-navigation-next").get_attribute('disabled') != 'true')
        if hasNextPage:

            nextPage = self.chrome.find_element_by_css_selector(".mat-paginator .mat-paginator-navigation-next")
            self.chrome.clickElement(nextPage)

            time.sleep(5)

            WebDriverWait(self.chrome, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".search-results__list"))
            )



        return hasNextPage

    def addJobsToArray(self, jobArray):
        while True:
            jobContainers = self.chrome.find_elements_by_css_selector(".job-results-container .search-result-item")
            for jobContainer in jobContainers:
                link = jobContainer.find_element_by_css_selector(".job-title-link").get_attribute("href")
                self.job.setLink(link)

                title = jobContainer.find_element_by_css_selector(".job-title").text
                self.job.setTitle(title)

                location = jobContainer.find_element_by_css_selector(".location").text
                self.job.setLocation(location)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                jobArray.append(self.job)
                self.job = Job()

            if self.nextPage():
                pass
            else:
                break

    def jobsForCompany(self):
        pass

    def loadJobs(self):
        self.loadScrapPage()
        try:
            self.addJobsToArray(self.jobs)

            self.chrome.getComplete("https://jobs.kaocareers.com/jobs?limit=100&location=United%20Kingdom&page=1&tags1=Molton%20Brown")

            WebDriverWait(self.chrome, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".search-results__list"))
            )

            self.addJobsToArray(self.moltonBrownJobs)

            self.sanitizeElementsForDescription()

            self.jobsForCompany()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())
                description = self.chrome.find_element_by_css_selector(".main-description-section .main-description-body").get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)

            return True
        except:
            self.exceptionLogging()
            return False
