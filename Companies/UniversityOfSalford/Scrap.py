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
        self.companyName = "University of Salford"
        self.ownerUsername = "universityofsalford"
        self.scrapPageURL = "https://eur01.safelinks.protection.outlook.com/?url=https%3A%2F%2Funiversityofsalford.tal.net%2Fvx%2Flang-en-GB%2Fmobile-0%2Fappcentre-ext%2Fbrand-4%2Fxf-2862b5dce5ca%2Fcandidate%2Fjobboard%2Fvacancy%2F3%2Fadv%2F&data=05%7C01%7Cv.p.hindmarch%40salford.ac.uk%7C0f36ba03075b4a8ef2ad08dad7818602%7C65b52940f4b641bd833d3033ecbcf6e1%7C0%7C0%7C638059248577415697%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&sdata=fO8T%2BJoLD3WkkYpgsQHgdYtgzEgUPakyMuooMnFumB0%3D&reserved=0"
        self.feedType = self.feedTypeWebScrap
        self.jobKey = 'title'
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".search-results #tile-results-list"))
        )


    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector(".search-results #tile-results-list li")
            for jobContainer in jobContainers:
                title = jobContainer.find_element_by_css_selector(".search_res h3 a").text
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector(".search_res h3 a").get_attribute('href')
                self.job.setLink(link)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, currentJobInfo in enumerate(self.jobs):
                self.chrome.getComplete(currentJobInfo.getLink())

                self.sanitizeElementsForDescription()

                jobDataFields = self.chrome.find_elements_by_css_selector(".hform_section .hform_field_label_pos_left")
                for jobDataField in jobDataFields:
                    fieldName = jobDataField.find_element_by_css_selector('.eform_field_label ').text
                    if 'Salary' in fieldName:
                        salary = jobDataField.find_element_by_css_selector('.form_value').text
                        self.jobs[currentJobIndex].setSalary(salary)

                    if 'Primary Location' in fieldName:
                        location = jobDataField.find_element_by_css_selector('.form_value').text
                        self.jobs[currentJobIndex].setLocation(location)

                    if 'Opportunity' in fieldName:
                        description = jobDataField.find_element_by_css_selector('.form_value').text
                        self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False