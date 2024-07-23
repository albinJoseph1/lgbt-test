# Required Packages
from Resource import htmlmin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "AEG Europe"
        self.ownerUsername = "aegeurope"
        self.scrapPageURL = "https://aegeurope.earcu.com/jobs/vacancy/find/results/"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ListGridContainer"))
        )


    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()
        try:

            jobContainers = self.chrome.find_elements_by_css_selector(".rowContainerHolder")
            for jobContainer in jobContainers:
                title = str(jobContainer.find_element_by_css_selector(".rowHeader").text)
                title = title.strip()
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector(".rowHeader a").get_attribute("href")
                self.job.setLink(link)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                location = self.chrome.find_element_by_css_selector('.posdescriptionPropertyBox .SumItem_codelist5value .jobSumValue').text
                self.jobs[currentJobIndex].setLocation(location)

                salary = self.chrome.find_element_by_css_selector('.posdescriptionPropertyBox .SumItem_displaysalarydescription .jobSumValue').text
                self.jobs[currentJobIndex].setSalary(salary)

                expireDate =self.chrome.find_element_by_css_selector('.posdescriptionPropertyBox .SumItem_pospublishenddate .jobSumValue').text
                possibleExpiryDateFormats = [
                    "%d %B %Y"
                ]
                for possibleExpireDate in possibleExpiryDateFormats:
                    try:
                        expireDate = datetime.strptime(expireDate, possibleExpireDate).strftime('%Y-%m-%d')
                        self.jobs[currentJobIndex].setExpireDate(expireDate)
                    except Exception as e:
                        exception_message = str(title) + ' : ' + str(e) + "\n"
                        self.exceptionLogging('warning', exception_message)

                self.sanitizeElementsForDescription()

                description = self.chrome.find_element_by_css_selector(".PosDescriptionText .earcu_posdescriptionContainer").get_attribute("innerHTML") + self.chrome.find_element_by_css_selector(".PosDescriptionText .arrowList").get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)

            return True


        except:
            self.exceptionLogging()
            return False