# Required Packages
import time
import re

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
        self.companyName = "UKTV"
        self.ownerUsername = "uktv"
        self.scrapPageURL = "https://my.corehr.com/pls/uktvrecruit/erq_search_package.search_form?p_company=1&p_internal_external=E"
        self.feedType = self.feedTypeWebScrap
        self.parameterToUrl = "?"
        self.jobLink = "https://my.corehr.com/pls/uktvrecruit/erq_jobspec_version_4.display_form"
        self.location = "London"
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".erq_table_no_top_border"))
        )

        searchButton = self.chrome.find_element_by_css_selector(".erq_table_no_top_border .erq_small_button")
        self.chrome.clickElement(searchButton)

        jobSpecFormFields = self.chrome.find_elements_by_css_selector("form[name='callTheJobSpecFromSearch'] input")
        for jobSpecFormField in jobSpecFormFields:
            fieldName = jobSpecFormField.get_attribute('name')
            fieldValue = jobSpecFormField.get_attribute('value')
            if 'p_recruitment_id' not in fieldName:
                self.parameterToUrl = self.parameterToUrl + fieldName + "=" + fieldValue
                self.parameterToUrl = self.parameterToUrl + "&"

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector(".erq_table_no_top_border > tbody > tr")
            for jobContainer in jobContainers:
                isJobRow = bool(jobContainer.find_elements_by_css_selector(".erq_searchv4_result_row"))
                if isJobRow:
                    title = jobContainer.find_element_by_css_selector("a.erq_searchv4_big_anchor").text
                    self.job.setTitle(title)

                    jobId = jobContainer.find_element_by_css_selector("a.erq_searchv4_big_anchor").get_attribute('href').split("'")[1::2][0]
                    link = self.jobLink + self.parameterToUrl + "p_recruitment_id=" + jobId
                    self.job.setLink(link)

                    self.job.setLocation( self.location )

                    self.job.setOwnnerUsername(self.ownerUsername)
                    self.job.setCompanyName(self.companyName)

                    self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                description = self.chrome.find_element_by_css_selector(".erq_table_no_top_border .erq_searchv4_heading2").get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)

            return True
        except:
            self.exceptionLogging()
            return False