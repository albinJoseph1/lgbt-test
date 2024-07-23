# Required Packages
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

        self.companyName = "Ingeus"
        self.ownerUsername = "ingeus"
        self.scrapPageURL = "https://careers.ingeus.co.uk/en/listing/"
        self.jobIndicesToRemove = []
        self.feedType = self.feedTypeWebScrap

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        totalJobCount = int(self.chrome.find_element_by_css_selector("#recent-jobs .searchResultsNumber .result-count").text)
        self.chrome.getComplete(self.scrapPageURL + "?page=1&page-items=" + str(totalJobCount))

        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.ID, 'recent-jobs-content'))
        )

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector("#recent-jobs-content>div")
            for jobContainer in jobContainers:
                jobTitle = jobContainer.find_element_by_css_selector(".title").text
                self.job.setTitle(jobTitle)
                jobLocation = jobContainer.find_element_by_css_selector("div.location span.location").text
                self.job.setLocation(jobLocation)
                jobLink = jobContainer.find_element_by_css_selector(".button a.job-link").get_attribute("href")
                self.job.setLink(jobLink)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, currentJobInfo in enumerate(self.jobs):
                self.chrome.getComplete(currentJobInfo.getLink())

                self.sanitizeElementsForDescription()

                try:
                    jobContract = self.chrome.find_element_by_css_selector(".work-type").text
                except:
                    jobContract = None
                self.jobs[currentJobIndex].setContract(jobContract)

                try:
                    jobSalary = self.chrome.find_element_by_css_selector(".locationContainer").text.split('\n')
                    if len(jobSalary) >= 2:
                        jobSalary = self.chrome.find_element_by_css_selector(".locationContainer").text.split('\n')[1]
                        self.jobs[currentJobIndex].setSalary(jobSalary)
                except:
                    pass

                try:
                    description = self.chrome.find_element_by_css_selector("#job-details").get_attribute('innerHTML')
                    self.jobs[currentJobIndex].setDescription(description)
                except:
                    self.jobIndicesToRemove.append(currentJobIndex)

                for currentIndex, jobIndexToRemove in enumerate(self.jobIndicesToRemove):
                    del self.jobs[jobIndexToRemove - currentIndex]

            return True
        except:
            self.exceptionLogging()
            return False