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
        self.jobCount = 0

        self.companyName = "General Mills"
        self.ownerUsername = "generalmills"
        self.scrapPageURL = "https://careers.generalmills.com/careers/jobs?country=United%20Kingdom"
        self.locationFilter = "United Kingdom"
        self.feedType = self.feedTypeWebScrap
        self.maxScrapPageLimit = 10

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        hasCookie = bool(self.chrome.find_elements_by_css_selector("div[aria-label='cookieconsent']"))
        if hasCookie:
            cookieCloseButton = self.chrome.find_element_by_css_selector("div[aria-label='cookieconsent'] a[aria-label='dismiss cookie message']")
            self.chrome.clickElement(cookieCloseButton)
        WebDriverWait(self.chrome, self.maxScrapPageLimit).until(
            EC.presence_of_element_located((By.ID, 'filterBar'))
        )

    def navigateToNextPage(self):
        hasNextPage = bool(self.chrome.find_element_by_css_selector(".mat-paginator-range-actions .mat-paginator-navigation-next").is_enabled())
        if hasNextPage:
            nextButton = self.chrome.find_element_by_css_selector(".mat-paginator-range-actions .mat-paginator-navigation-next")
            self.chrome.clickElement(nextButton)
            WebDriverWait(self.chrome, self.maxScrapPageLimit).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".job-results-container"))
            )
            return True
        else:
            return False

    def loadJobs(self):
        self.loadScrapPage()
        try:
            while True:
                allJobs = WebDriverWait(self.chrome, 100).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".job-results-container"))
                )
                jobContainers = allJobs.find_elements_by_css_selector(".search-result-item")
                for jobContainer in jobContainers:
                    jobTitle = jobContainer.find_element_by_css_selector(".job-title").text
                    self.job.setTitle(jobTitle)
                    jobLink = jobContainer.find_element_by_css_selector(".job-title a").get_attribute("href")
                    self.job.setLink(jobLink)
                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

                if self.navigateToNextPage():
                    pass
                else:
                    break

            jobIndex = 0
            for job in self.jobs:
                self.chrome.getComplete(job.getLink())

                try:
                    WebDriverWait(self.chrome, 100).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".job-description-container"))
                    )

                    isJobExists = True
                except:
                    isJobExists = False

                if isJobExists:
                    jobLocations = self.chrome.find_element_by_css_selector("#header-locations").text
                    jobLocations = jobLocations.split(';')
                    for jobLocation in jobLocations:
                        if self.locationFilter in jobLocation:
                            jobLocation.strip()
                            self.jobs[jobIndex].setLocation(jobLocation)

                    self.sanitizeElementsForDescription()

                    jobDescription = self.chrome.find_element_by_css_selector(".main-description-section").get_attribute('innerHTML')
                    self.jobs[jobIndex].setDescription(jobDescription)

                    jobIndex = jobIndex + 1
                else:
                    del self.jobs[jobIndex]

            return True
        except:
            self.exceptionLogging()
            return False