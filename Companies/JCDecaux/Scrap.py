# Required Packages
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "JCDecaux"
        self.ownerUsername = "jcdecaux"
        self.scrapPageURL = "https://www.jcdecauxcareers.co.uk/jobs/ajaxaction/posbrowser_gridhandler/?movejump=1&movejump_page=1&pagestamp=6c349f09-90bd-4e77-8446-58db419e56e3"
        self.feedType = self.feedTypeWebScrap
        self.count = 1
        self.totalPages = ""
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gridTableContainer"))
        )

    def nextPage(self):
        if int(self.count) == int(self.totalPages):
            return False
        else:
            self.count = self.count + 1
            self.scrapPageURL = "https://www.jcdecauxcareers.co.uk/jobs/ajaxaction/posbrowser_gridhandler/?movejump=1&movejump_page=" + str(self.count) + "&pagestamp=6c349f09-90bd-4e77-8446-58db419e56e3"
            self.loadScrapPage()
            return True


    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()
        totalPages = self.chrome.find_element_by_css_selector(".pagingText").text
        self.totalPages = totalPages.split("Page 1 of ")[1]

        try:
            while True:
                jobContainers = self.chrome.find_elements_by_css_selector(".gridTableContainer .rowContainer")
                for jobContainer in jobContainers:
                    title = jobContainer.find_element_by_css_selector(".rowHeader a").text
                    self.job.setTitle(title)

                    link = jobContainer.find_element_by_css_selector(".rowHeader a").get_attribute('href')
                    self.job.setLink(link)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

                if self.nextPage():
                    pass
                else:
                    break

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                jobProperties = self.chrome.find_elements_by_css_selector(".posdescriptionPropertyBox .jobSum li")
                for jobProperty in jobProperties:
                    itemLabel = jobProperty.find_element_by_css_selector('.jobSumLabel').text
                    if 'Location' in itemLabel:
                        location = jobProperty.find_element_by_css_selector('.jobSumValue').text
                        self.jobs[currentJobIndex].setLocation(location)
                        break

                elementToRemove = []
                elementsToBeRemoved = ['.ApplyNowContainer .buttonAnchor']
                for element in elementsToBeRemoved:
                    hasElement = bool(self.chrome.find_elements_by_css_selector(element))
                    if hasElement:
                        elementToBeRemoved = self.chrome.find_element_by_css_selector(element)
                        elementToRemove.append(elementToBeRemoved)

                self.sanitizeElementsForDescription(elementToRemove)

                description = self.chrome.find_element_by_css_selector(".PosDescriptionText").get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)

            return True
        except:
            self.exceptionLogging()
            return False