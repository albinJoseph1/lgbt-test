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
        self.companyName = "HMRC"
        self.ownerUsername = "hmrc"
        self.scrapPageURL = "https://www.civilservicejobs.service.gov.uk/csr/index.cgi?SID=dXNlcnNlYXJjaGNvbnRleHQ9MTUzNDAyMTM5Jm93bmVyPTUwNzAwMDAmb3duZXJ0eXBlPWZhaXImcGFnZWNsYXNzPUpvYnMmcGFnZWFjdGlvbj1zZWFyY2hieWNvbnRleHRpZCZyZXFzaWc9MTY1MDIxMjc1Ni1iNThjMDA2YTFjNGFiNWNlMmU5MDg4NTFiY2QxNWM4NTQwZTAxMTg5"
        self.feedType = self.feedTypeWebScrap
        self.organisation = "HM Revenue and Customs"
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        #
        # selectDistance = Select(self.chrome.find_element_by_css_selector("select[name='postcodedistance']"))
        # selectDistance.select_by_visible_text("600")
        #
        # organisationSelectBox = self.chrome.find_element_by_css_selector("span[aria-label=Organisation]")
        # self.chrome.clickElement(organisationSelectBox)
        # organisationOptions = self.chrome.find_elements_by_css_selector(
        #     ".select2-results #select2-nghr_dept-results li")
        # self.chrome.execute_script(
        #     "jQuery('.select2-results #select2-nghr_dept-results').css('max-height','100%');")
        # for organisationOption in organisationOptions:
        #     organisation = organisationOption.text
        #     if organisation in self.organisation:
        #         hoverToOption = ActionChains(self.chrome).move_to_element(organisationOption)
        #         hoverToOption.perform()
        #         self.chrome.clickElement(organisationOption)
        #         break
        #
        # submitButton = self.chrome.find_element_by_css_selector("#submitSearch")
        # self.chrome.clickElement(submitButton)


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
                jobContainers = self.chrome.find_elements_by_css_selector("ul .search-results-job-box")
                jobLink = "https://www.civilservicejobs.service.gov.uk/csr/jobs.cgi?vxsys=4&vxvac="
                for jobContainer in jobContainers:
                    title = jobContainer.find_element_by_css_selector(".search-results-job-box-title").text
                    self.job.setTitle(title)

                    link = jobContainer.find_element_by_css_selector(".search-results-job-box-refcode").text
                    link = link.strip("Reference: ")
                    link = jobLink + link
                    self.job.setLink(link)

                    location = jobContainer.find_element_by_css_selector(".search-results-job-box-location").text
                    location = location.split(",")[0]
                    self.job.setLocation(location)

                    salary = jobContainer.find_element_by_css_selector(".search-results-job-box-salary").text
                    salary = salary.split("Salary : ")[1]
                    self.job.setSalary(salary)

                    hasExpireDate = bool(
                        jobContainer.find_elements_by_class_name("search-results-job-box-closingdate"))

                    if hasExpireDate:
                        expireDate = None
                        expire = jobContainer.find_element_by_css_selector(
                            ".search-results-job-box-closingdate").text
                        expire = expire.split("Closes : ")[1]

                        possibleExpiryDateFormats = [
                            "%H:%M pm on %A %dth %B %Y",
                            "%H:%M pm on %A %dst %B %Y",
                            "%H:%M pm on %A %drd %B %Y",
                            "%H:%M pm on %A %dnd %B %Y",
                            "%H:%M am on %A %dth %B %Y",
                            "%H:%M am on %A %dst %B %Y",
                            "%H:%M am on %A %drd %B %Y",
                            "%H:%M am on %A %dnd %B %Y",
                        ]
                        for possibleExpireDate in possibleExpiryDateFormats:
                            try:
                                expireDate = datetime.strptime(expire, possibleExpireDate).strftime('%Y-%m-%d')
                            except Exception as e:
                                exception_message = str(title) + ' : ' + str(e) + "\n"
                                self.exceptionLogging('warning', exception_message)
                        self.job.setExpireDate(expireDate)

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