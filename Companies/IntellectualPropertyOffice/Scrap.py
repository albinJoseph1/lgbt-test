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
        self.companyName = "Intellectual Property Office"
        self.ownerUsername = "intellectualpropertyoffice"
        self.scrapPageURL = "https://www.civilservicejobs.service.gov.uk/csr/index.cgi?SID=cGFnZWFjdGlvbj1zZWFyY2hjb250ZXh0Jm93bmVyPTUwNzAwMDAmb3duZXJ0eXBlPWZhaXImY29udGV4dGlkPTcwNjgxMzIyJnBhZ2VjbGFzcz1TZWFyY2gmcmVxc2lnPTE3MDg5NDMxNDEtNzNmMWNkZDZjYTU3NTJiZGE2OTk4ZTIzNDhmNGM0ZmM2ZDAxMjIwYg=="
        self.feedType = self.feedTypeWebScrap
        self.organisation = "Intellectual Property Office"
        self.location = "London"
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        try:
            cookieSection = WebDriverWait(self.chrome, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#csr-cookie-message #accept_all_cookies_button"))
            )
            cookieSection.click()
        except Exception as e:
            exception_message = str(e) + "\n"
            self.exceptionLogging('warning', exception_message)

        try:
            searchField = self.chrome.find_element_by_name("where")
            searchField.send_keys(self.location)
            searchField.submit()
        except Exception as e:
            exception_message = str(e) + "\n"
            self.exceptionLogging('warning', exception_message)

        distanceFilter = self.chrome.find_element_by_css_selector("[data-oselect-type='location'] button")
        self.chrome.clickElement(distanceFilter)
        selectDistance = Select(self.chrome.find_element_by_css_selector("#ID_csr_form_postcodedistance"))
        selectDistance.select_by_value("600")

        multiSelectors = self.chrome.find_elements_by_css_selector("[data-oselect-type='multiselect']")
        for multiselector in multiSelectors:
            selectorText = multiselector.find_element_by_css_selector('button').text
            if 'Department' in selectorText:
                deptFilter = multiselector.find_element_by_css_selector('button')
                self.chrome.clickElement(deptFilter)
                self.chrome.execute_script("""
                                   jQuery('.oselect__available-options-list').css({'overflow-y':'inherit','overflow-x':'inherit'});
                                   """)
                listOfDepts = multiselector.find_elements_by_css_selector('.oselect__available-options-list li')
                for department in listOfDepts:
                    if self.organisation in department.text:

                        self.chrome.clickElement(department.find_element_by_css_selector('input'))

        submitButton = self.chrome.find_element_by_css_selector("#submitSearchUpdate")
        self.chrome.clickElement(submitButton)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-results-panel-main"))
        )


    def nextPage(self):

        has_next_button = bool(self.chrome.find_elements_by_css_selector('.search-results-pageform-pages b ~ a'))

        if has_next_button:
            next_button = self.chrome.find_element_by_css_selector('.search-results-pageform-pages b ~ a')
            has_next_page = bool(self.chrome.find_elements_by_css_selector('.search-results-pageform-pages a:last-child'))
            if has_next_page:
                next_button.click()
                self.chrome.pageWait()
                return has_next_page
            else:
                return False


    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()
        try:
            while True:
                jobContainers = self.chrome.find_elements_by_css_selector(".search-results-panel-main ul[title='Job list'] li")
                for jobContainer in jobContainers:
                    title = jobContainer.find_element_by_css_selector(".search-results-job-box-title").text
                    self.job.setTitle(title)

                    link = jobContainer.find_element_by_css_selector(".search-results-job-box-title > a").get_attribute("href")
                    self.job.setLink(link)

                    location = jobContainer.find_element_by_css_selector(".search-results-job-box-location").text
                    self.job.setLocation(location)

                    salary = jobContainer.find_element_by_css_selector(".search-results-job-box-salary").text
                    salary = salary.split("Salary : ")[1]
                    self.job.setSalary(salary)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()
                if self.nextPage():
                    pass
                else:
                    break

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                elementToRemove = []
                elementsToBeRemoved = ['.vac_display_section_heading:first-child',
                                       '.vac_display_field_value:first-child',
                                       '#vac_advert_logo_block_standard',
                                       '.some_new_classname',
                                       '.vac_display_attachments',
                                       '.vac_display_apply',
                                       '#vac_advert_logo_block_mobile'
                                       ]
                for element in elementsToBeRemoved:
                    hasElement = bool(self.chrome.find_elements_by_css_selector(
                        ".vac_display_panel_main_inner "+element))
                    if hasElement:
                        elementToBeRemoved = self.chrome.find_element_by_css_selector(
                            ".vac_display_panel_main_inner "+element)
                        elementToRemove.append(elementToBeRemoved)

                self.sanitizeElementsForDescription(elementToRemove)

                description = self.chrome.find_element_by_css_selector(".vac_display_panel_main_inner").get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)

            return True
        except:
            self.exceptionLogging()
            return False
