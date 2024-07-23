# Required Packages
from datetime import datetime
from Resource import htmlmin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Bromford"
        self.ownerUsername = "bromford"
        self.scrapPageURL = "https://www.bromford.co.uk/about-us/jobs/current-vacancies/"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".job-listing"))
        )

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector(".job-listing a")
            for jobContainer in jobContainers:
                title = jobContainer.find_element_by_css_selector(".job-listing__job__title").text
                self.job.setTitle(title)

                link = jobContainer.get_attribute('href')
                self.job.setLink(link)

                jobDetails = jobContainer.find_elements_by_css_selector("div p")
                for jobDetail in jobDetails:
                    jobDetailValue = jobDetail.text
                    if 'Location' in jobDetailValue:
                        jobDetailValue = jobDetailValue.split(":")[1].strip()
                        self.job.setLocation(jobDetailValue)

                    if 'Salary' in jobDetailValue:
                        jobDetailValue = jobDetailValue.split(":")[1].strip()
                        self.job.setSalary(jobDetailValue)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())
                try:

                    WebDriverWait(self.chrome, 100).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".PLACEHOLDER"))
                    )

                    self.sanitizeElementsForDescription()

                    description = self.chrome.find_element_by_css_selector(".container.PLACEHOLDER").get_attribute('innerHTML')
                    self.jobs[currentJobIndex].setDescription(description)
                except:
                    WebDriverWait(self.chrome, 100).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".AdvertParentContainer > div:nth-last-child(4)"))
                    )

                    self.sanitizeElementsForDescription()

                    description = self.chrome.find_element_by_css_selector(".PLACEHOLDER").get_attribute('innerHTML')
                    self.jobs[currentJobIndex].setDescription(description)

            return True
        except:
            self.exceptionLogging()
            return False
