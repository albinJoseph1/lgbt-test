# Required Packages
from Resource import htmlmin
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
        self.companyName = "ICON"
        self.ownerUsername = "prahealthsciences"
        self.scrapPageURL = "https://prahs.com/careers/search"
        self.location = "United Kingdom"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".list--careers"))
        )

        #     Removing instabot section
        has_widget = bool(self.chrome.find_elements_by_css_selector('.roko-instabot-widget'))
        if has_widget:
            self.chrome.execute_script("""
                               jQuery('.roko-instabot-widget').remove();
                               """)

            self.chrome.execute_script("""
                               jQuery('.roko-instabot-overlay').remove();
                               """)

            self.chrome.execute_script("""
                                jQuery('.roko-instabot-widget-button').remove()
                                """)

        # Closing cookie section
        hasCookie = bool(self.chrome.find_elements_by_css_selector("#onetrust-banner-sdk"))
        if hasCookie:
            cookieClose = self.chrome.find_element_by_css_selector(
                "#onetrust-banner-sdk #onetrust-accept-btn-handler").click()

        time.sleep(2)

        # Closing Modal
        hasModal = bool(self.chrome.find_elements_by_css_selector(".modal .z-50"))
        if hasModal:
            ModalClose = self.chrome.find_element_by_css_selector(".modal .z-50 .modal-close").click()

        self.chrome.execute_script("""
                            jQuery('.filters .filters__selectr .multiselect__content').css('max-height','100%')
                            """)

        self.chrome.find_element_by_css_selector(".filters .multiselect:nth-of-type(1) .multiselect__tags").click()


        # Filtering Jobs
        filterElements = self.chrome.find_elements_by_css_selector(".filters .multiselect:nth-of-type(1) .multiselect__element")
        for filterElement in filterElements:
            filterText = filterElement.find_element_by_css_selector(".multiselect__option span").text
            if filterText == 'United Kingdom':
                filterElement.find_element_by_css_selector(".multiselect__option span").click()

        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".results.js-results"))
        )

    def nextPage(self):

        has_next = bool(self.chrome.find_elements_by_css_selector(".pagination .paginate-links > li:nth-child(2)"))
        if(has_next):
            has_next_page = self.chrome.find_element_by_css_selector(
                ".pagination .paginate-links > li:nth-child(2)").get_attribute('class') != "next disabled"
        else:
            return False
        if has_next_page:
            self.chrome.find_element_by_css_selector('.pagination .next').click()
            time.sleep(2)
            return has_next_page
        else:

            return False

    def loadJobs(self):
        self.loadScrapPage()
        try:
            while True:

                jobContainers = self.chrome.find_elements_by_css_selector(".list--careers .card--career")
                for jobContainer in jobContainers:
                    title = str(jobContainer.find_element_by_css_selector(".card__title").text)
                    title = title.strip()
                    self.job.setTitle(title)

                    link = jobContainer.find_element_by_css_selector(".career-id").text
                    link = link.split(':')
                    link = link[1].strip()
                    link = 'https://prahs.com/careers/id/' + link
                    self.job.setLink(link)

                    self.job.setLocation(self.location)
                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()


                if self.nextPage():
                    pass
                else:
                    break

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                elementsToRemove = []
                elementsTobeRemoved = [".border-b", ".gtm-apply", "p.text-xs"]
                for element in elementsTobeRemoved:
                    hasElementPresent = bool(self.chrome.find_elements_by_css_selector(element))
                    if hasElementPresent:
                        elementsToRemove.append(self.chrome.find_element_by_css_selector(element))
                self.sanitizeElementsForDescription(elementsToRemove)

                description = self.chrome.find_element_by_css_selector(".section.-two-column > div:nth-child(2)").get_attribute('innerHTML')

                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False
