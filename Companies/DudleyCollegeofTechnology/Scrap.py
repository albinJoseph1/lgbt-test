from datetime import datetime
# Required Packages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Companies.StandardAgent import ScrapAgent
import re

POSSIBLEEXPIRYDATEFORMATS = [
    "%d/%m/%y",
]
class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.jobCount = 0

        self.companyName = "Dudley College of Technology"
        self.ownerUsername = "dudleycollegeoftechnology"
        self.scrapPageURL = "https://dudleycol.ac.uk/our-college/jobs/vacancies/"
        self.jobIndicesToRemove = []
        self.feedType = self.feedTypeWebScrap

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.boxed-content'))
        )

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector(".boxed-content-wrap .boxed-content")
            for jobContainer in jobContainers:
                jobTitle = jobContainer.find_element_by_css_selector(".page-title").text
                self.job.setTitle(jobTitle)
            
                jobLink = jobContainer.find_element_by_css_selector(".entry-content a").get_attribute("href")
                self.job.setLink(jobLink)

                closingDateElement = jobContainer.find_element_by_css_selector(".meta")
                if closingDateElement:
                    extractExpireDate = closingDateElement.text.strip().replace('Closing: ', '')
                    for possibleExpireDate in POSSIBLEEXPIRYDATEFORMATS:
                        try:
                            extractExpireDate = datetime.strptime(extractExpireDate, possibleExpireDate).strftime('%Y-%m-%d')
                            self.job.setExpireDate(extractExpireDate)
                            break
                        except Exception as e:
                            exception_message = str(self.job.getTitle()) + ' : ' + str(e) + "\n"
                            self.exceptionLogging('warning', exception_message)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                jobLocation = self.chrome.find_element_by_css_selector("#MergeCore_MergeField1").text.split('Location:')[1]
                self.jobs[currentJobIndex].setLocation(jobLocation)

                jobSalary = self.chrome.find_element_by_css_selector(".rounded-bottom #MergeCore_MergeField2").text.split('Salary:')[1]
                self.jobs[currentJobIndex].setSalary(jobSalary)

                jobDescription = self.chrome.find_element_by_css_selector(".container.PLACEHOLDER").get_attribute('innerHTML')
                self.jobs[currentJobIndex].setDescription(jobDescription)

            return True
        except:
            self.exceptionLogging()
            return False