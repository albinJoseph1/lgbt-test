# Required Packages
from datetime import datetime
from Resource import htmlmin
from selenium.webdriver.support.ui import Select
import time
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
        self.companyName = "Channeladvisor"
        self.ownerUsername = "channeladvisor"
        self.scrapPageURL = "https://careers-channeladvisor.icims.com/jobs/search?ss=1&searchLocation=13267-14967-Limerick"
        self.locationValue = ['13702--London', '13267-14967-Limerick']
        self.feedType = self.feedTypeWebScrap
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        self.chrome.switch_to.frame(0)

    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()
        self.chrome.pageWait()
        location_value = self.locationValue

        try:
            for value in location_value:
                location = Select(self.chrome.find_element_by_xpath('//*[@id="jsb_f_location_s"]'))
                location.select_by_value(value)
                search = self.chrome.find_element_by_xpath('//*[@id="jsb_form_submit_i"]')
                search.click()

                jobContainers = self.chrome.find_elements_by_css_selector(".iCIMS_JobsTable .row")
                for jobContainer in jobContainers:
                    title = str(jobContainer.find_element_by_css_selector(".col-xs-12.title > a > h2").text)
                    title = title.strip()
                    self.job.setTitle(title)

                    link = jobContainer.find_element_by_css_selector(".col-xs-12.title > a").get_attribute("href")
                    self.job.setLink(link)

                    location = jobContainer.find_element_by_css_selector(".col-xs-6.header.left > span:last-child").text
                    self.job.setLocation(location)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())
                self.chrome.switch_to.frame(0)

                tableElement = self.chrome.find_element_by_css_selector(".container-fluid.iCIMS_JobsTable")
                logoElement = self.chrome.find_element_by_css_selector(".iCIMS_Logo")
                optionsElement = self.chrome.find_element_by_css_selector(".iCIMS_JobOptions")
                elementToRemove = [tableElement,logoElement,optionsElement]
                self.sanitizeElementsForDescription(elementToRemove)

                descriptionElement = self.chrome.find_element_by_class_name("iCIMS_JobContent")
                description = descriptionElement.get_attribute('innerHTML')
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False

