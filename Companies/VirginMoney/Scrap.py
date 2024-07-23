# Required Packages
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage=None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Virgin Money"
        self.ownerUsername = "virginmoney"
        self.scrapPageURL = "https://vacancies.virginmoney.com/en/listing/"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        totalJobCount = int(self.chrome.find_element_by_css_selector("#recent-jobs .more-link").get_attribute("data-page-items")) + int( self.chrome.find_element_by_css_selector("#recent-jobs .more-link .count").text)
        self.chrome.getComplete(self.scrapPageURL+"?page=1&page-items="+str(totalJobCount))

        hasCookie = bool(self.chrome.find_elements_by_css_selector(".js-cookieMsg__btn"))
        if hasCookie:
            cookieClose = self.chrome.find_element_by_css_selector(".js-cookieMsg__btn")
            self.chrome.clickElement(cookieClose)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#recent-jobs-content"))
        )

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector("#recent-jobs-content li")
            for jobContainer in jobContainers:
                link = jobContainer.find_element_by_css_selector("p:first-child a").get_attribute('href')
                self.job.setLink(link)

                title = jobContainer.find_element_by_css_selector("p:first-child a").text
                self.job.setTitle(title)

                location = jobContainer.find_element_by_css_selector(".location").text
                self.job.setLocation(location)

                contract = jobContainer.find_element_by_css_selector(".work-type").text
                self.job.setContract(contract)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                salary = self.chrome.find_element_by_css_selector("#job-details").text
                salary = salary.splitlines()
                for i in range(len(salary)):
                    if 'Salary' in salary[i]:
                        salary = salary[i]
                        if ':' in salary:
                            salary = salary.split(":")[1].strip()
                        else:
                            salary = salary.split("Salary")[1].strip()
                        break
                self.jobs[currentJobIndex].setSalary(salary)

                description = self.chrome.find_element_by_css_selector("#job-details").get_attribute('innerHTML')
                self.jobs[currentJobIndex].setDescription(description)

            return True
        except:
            self.exceptionLogging()
            return False