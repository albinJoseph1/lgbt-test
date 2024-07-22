# Required Packages
from Resource import htmlmin
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
        self.companyName = "Merlin Entertainments"
        self.ownerUsername = "merlinentertainment"
        self.scrapPageURL = "https://www.merlincareers.com/en/job-search-results?c=merlin&Country=United+Kingdom&page=0"
        self.feedType = self.feedTypeWebScrap
        self.maxScrapPageLimit = 20
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search__container__right"))
        )


    def nextPage(self):
        try:
            next_button = self.chrome.find_element_by_css_selector('.jobs-pager > a:last-child')
        except:
            return False

        has_next_page = next_button.get_attribute("class") != ' disabled'
        if has_next_page:
            next_button.click()
            time.sleep(3)
            WebDriverWait(self.chrome, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search__container__right"))
            )
            return has_next_page
        else:
            return False

    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()
        try:
            while True:
                jobContainers = self.chrome.find_elements_by_css_selector(".jobs-search__container .job-summary")
                for jobContainer in jobContainers:
                    title = str(jobContainer.find_element_by_css_selector(".job-summary__details__content__title h3").text)
                    title = title.strip()
                    self.job.setTitle(title)

                    link = jobContainer.find_element_by_css_selector(".job-summary__details__cta a").get_attribute('href')
                    self.job.setLink(link)

                    jobLocation = jobContainer.find_element_by_css_selector(".job-summary__details__content__title p").text

                    self.job.setLocation(jobLocation)
                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

                if self.nextPage():
                    pass
                else:
                    break

            jobIndex = 0
            for job in self.jobs:
                self.chrome.getComplete(job.getLink())

                isJobExists = bool(self.chrome.find_elements_by_class_name("c-job-detail__body__details"))
                if isJobExists:
                    anchorElement = self.chrome.find_element_by_css_selector('.c-job-detail__body__details a:last-child')
                    elementToRemove = [anchorElement]
                    self.sanitizeElementsForDescription(elementToRemove)

                    descriptionElement = self.chrome.find_element_by_class_name("c-job-detail__body__details")
                    description = descriptionElement.get_attribute('innerHTML')
                    description = description.replace("\n", "")
                    self.jobs[jobIndex].setDescription(description)

                    jobIndex = jobIndex + 1
                else:
                    del self.jobs[jobIndex]

            return True
        except:
            self.exceptionLogging()
            return False
