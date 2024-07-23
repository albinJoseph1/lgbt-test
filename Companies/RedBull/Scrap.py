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
        self.companyName = "RedBull"
        self.ownerUsername = "redbull"
        self.scrapPageURL = "https://jobs.redbull.com/gb-en/results?functions=&locations=2060&locationNames=United%20Kingdom,%20Europe&keywords="
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-id = 'search-results']"))
        )

    def loadJobs(self):
        self.loadScrapPage()

        try:
            jobContainersBeforeLoad = 0
            while True:
                loadMoreButton = self.chrome.find_element_by_css_selector("[data-id = 'search-results'] .SearchResults_search-result__button-wrapper__2hOra button")
                self.chrome.clickElement(loadMoreButton)

                time.sleep(5)

                jobContainers = self.chrome.find_elements_by_css_selector("[data-id = 'search-results'] a[data-id='job-card']")
                jobContainersAfterLoad = len(jobContainers)
                if jobContainersAfterLoad == jobContainersBeforeLoad:
                    break
                else:
                    jobContainersBeforeLoad = jobContainersAfterLoad
                    pass

            for jobContainer in jobContainers:
                title = jobContainer.find_element_by_css_selector(".JobCard_job-card__title__UDBpP").text
                self.job.setTitle(title)

                link = jobContainer.get_attribute("href")
                self.job.setLink(link)

                location = jobContainer.find_element_by_css_selector(".JobCard_job-card__location__5zXZi").text
                self.job.setLocation(location)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()


            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                description = self.chrome.find_element_by_css_selector(".IntroCopy_intro-copy__GI10t").get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)

            return True
        except:
            self.exceptionLogging()
            return False