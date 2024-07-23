# Required Packages
from Resource import htmlmin
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from Managers import lgbtManager

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Trowers & Hamlins"
        self.ownerUsername = "trowershamlinsllp"
        self.scrapPageURL = "https://apply.trowers.com/vacancies/"
        self.locationFilters = ['Birmingham','Exeter','London','Manchester']
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        WebDriverWait(self.chrome, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".search-vacancies"))
        )

        self.chrome.clickElement(self.chrome.find_element_by_css_selector(".group-button-wrap #submit"))

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".vacancy-list"))
        )


    def nextPage(self):
        has_next_page = bool(self.chrome.find_elements_by_css_selector(".paginator .next-page"))
        if has_next_page:
            next_button = self.chrome.find_element_by_css_selector(".paginator .next-page")
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

                jobContainers = self.chrome.find_elements_by_css_selector('.vacancy-details')
                for jobContainer in jobContainers:
                    location = jobContainer.find_element_by_css_selector('.value_locations').text
                    jobNeedsToScrape = False
                    for locationFilter in self.locationFilters:
                        if locationFilter in location:
                            jobNeedsToScrape = True
                            break

                    if jobNeedsToScrape:
                        title = jobContainer.find_element_by_css_selector('.vacancy-title').text
                        self.job.setTitle(title)

                        link = jobContainer.find_element_by_css_selector('.apply_now').get_attribute('href')
                        self.job.setLink(link)

                        self.job.setLocation(location)

                        self.job.setOwnnerUsername(self.ownerUsername)

                        self.job.setCompanyName(self.companyName)

                        self.addToJobs()


                if self.nextPage():
                    pass
                else:
                    break

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())
                description = ""

                try:
                    intro_element = self.chrome.find_element_by_css_selector(".value_job_advert_description_intro")
                    description += intro_element.get_attribute("innerHTML")
                except NoSuchElementException:
                    pass

                try:
                    description_element = self.chrome.find_element_by_css_selector(".value_job_advert_description")
                    description += description_element.get_attribute("innerHTML")
                except NoSuchElementException:
                    pass

                try:
                    outro_element = self.chrome.find_element_by_css_selector(".value_job_advert_description_outro")
                    description += outro_element.get_attribute("innerHTML")
                except NoSuchElementException:
                    pass

                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False

