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
        self.companyName = "The Original Factory Shop"
        self.ownerUsername = "theoriginalfactoryshop"
        self.scrapPageURLs = ["http://www.tofscareers.com/vacancies/retail-vacancies-3/","http://www.tofscareers.com/vacancies/support-centre-vacancies-2/","http://www.tofscareers.com/vacancies/warehouse-vacancies-3/"]
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self,scrapPageURL):
        self.chrome.getComplete(scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#tableResults"))
        )


    def loadJobs(self):
        try:
            for scrapPageURL in self.scrapPageURLs:
                self.loadScrapPage(scrapPageURL)

                noJobsPresent = bool(self.chrome.find_elements_by_css_selector(".noadverts"))
                if noJobsPresent:
                    pass
                else:
                    jobContainers = self.chrome.find_elements_by_css_selector("#LoadingParent #tableResults tr")

                    for jobContainer in jobContainers:
                        title = jobContainer.find_element_by_css_selector(".vfjobtitle").text.split("(Reference:")[0].strip()
                        print(title)
                        self.job.setTitle(title)

                        link = jobContainer.find_element_by_css_selector(".vfapply button").get_attribute('onclick').split("OpenNewJob('")[1].split("');")[0]
                        print(link)
                        self.job.setLink(link)

                        location = jobContainer.find_element_by_css_selector(".vflocation").text
                        self.job.setLocation(location)

                        salary = jobContainer.find_element_by_css_selector(".vfsalary").text
                        self.job.setSalary(salary)

                        self.job.setCompanyName(self.companyName)
                        self.job.setOwnnerUsername(self.ownerUsername)

                        self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                description = self.chrome.find_element_by_css_selector("#pnlAdvertDetails .description").get_attribute('innerHTML')
                self.jobs[currentJobIndex].setDescription(description)

            return True
        except:
            self.exceptionLogging()
            return False
