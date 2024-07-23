# Required Packages
import time
from datetime import datetime
import datetime
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
        self.companyName = "Tribal"
        self.ownerUsername = "tribal"
        self.scrapPageURL = "https://www.tribalgroup.com/careers?category=&category=&region=Europe&region="
        self.feedType = self.feedTypeWebScrap
        self.locationFilter = ['UK','uk','Bristol','Norwich']
        self.titleExcludeFilter = ['internal','Internal']
        self.jobIndicesToRemove = []
        #     Company Details End

    def loadScrapPage(self):

        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#vacancyTop"))
        )

    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()

        try:
            jobContainers = self.chrome.find_elements_by_css_selector("#vacancyTop .grid-listing .grid-listing__item .post-summary--vacancy")
            for jobContainer in  jobContainers:
                title = jobContainer.find_element_by_css_selector(".post-summary__heading").text
                hasNoTitleFilter = True
                for titleFilter in self.titleExcludeFilter:
                    if titleFilter in title:
                        hasNoTitleFilter = False
                        break

                jobSummary = jobContainer.find_element_by_css_selector(".post-summary__figures").text
                jobSummary = jobSummary.splitlines()
                location = jobSummary[1].split("Location:")[1].strip()
                hasLocationFilter = False
                for locationFilter in self.locationFilter:
                    if locationFilter in location:
                        hasLocationFilter = True
                        break

                if hasNoTitleFilter and hasLocationFilter:
                    self.job.setTitle(title)

                    self.job.setLocation(location)

                    link = jobContainer.find_element_by_css_selector("a.post-summary__cta").get_attribute("href")
                    self.job.setLink(link)

                    salary = jobSummary[0].split("Salary:")[1].strip()
                    self.job.setSalary(salary)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                try:
                    WebDriverWait(self.chrome, 100).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".fsPage .fsSection"))
                    )

                    description = self.chrome.find_element_by_css_selector(".fsPage .fsSection").get_attribute('innerHTML')
                    self.jobs[currentJobIndex].setDescription(description)
                except:
                    self.jobIndicesToRemove.append(currentJobIndex)

            for currentIndex, jobIndexToRemove in enumerate(self.jobIndicesToRemove):
                del self.jobs[jobIndexToRemove - currentIndex]

            return True
        except:
            self.exceptionLogging()
            return False