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
        self.companyName = "GW Pharmaceuticals"
        self.ownerUsername = "gwpharmaceuticals"
        self.scrapPageURL = "https://careers.jazzpharma.com/jobs?location=United%20Kingdom&woe=12&stretchUnit=MILES&stretch=10&page=1"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jibe-container .job-results-container"))
        )
        # self.chrome.pageWait()

    def nextPage(self):
        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".mat-paginator"))
        )

        has_next_button = bool(self.chrome.find_element_by_css_selector('.mat-paginator .mat-paginator-range-actions .mat-paginator-navigation-next').get_attribute('class') == 'mat-focus-indicator mat-tooltip-trigger mat-paginator-navigation-next mat-icon-button mat-button-base' )

        if has_next_button:
            next_button = self.chrome.find_element_by_css_selector('.mat-paginator .mat-paginator-range-actions .mat-paginator-navigation-next')
            self.chrome.clickElement(next_button)
            time.sleep(2)
            return has_next_button
        else:
            return False

    def loadJobs(self):
        self.loadScrapPage()

        try:
            while True:
                jobContainers = self.chrome.find_elements_by_css_selector(".search-results .job-results-container .search-result-item")
                for jobContainer in jobContainers:


                    link = jobContainer.find_element_by_css_selector(".job-title a.job-title-link").get_attribute('href')
                    self.job.setLink(link)

                    title = jobContainer.find_element_by_css_selector(".job-title a.job-title-link").text
                    self.job.setTitle(title)

                    location = jobContainer.find_element_by_css_selector(".description-container .job-result__location .location").text
                    self.job.setLocation(location)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

                if self.nextPage():
                    pass
                else:
                    break

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                description = self.chrome.find_element_by_css_selector(".jibe-container .main-description-section").get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)


            return True

        except:
            self.exceptionLogging()
            return False