# Required Packages
from datetime import datetime
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
        self.companyName = "SeeAbility"
        self.ownerUsername = "seeability"
        self.scrapPageURL = "https://careers.seeability.org/vacancies/vacancy-search-results.aspx"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.delete_all_cookies()
        self.chrome.getComplete(self.scrapPageURL)
        self.chrome.pageWait()

        hasCookieSection = bool(self.chrome.find_elements_by_css_selector("#epdsubmit"))
        if hasCookieSection:
            cookieAccept = self.chrome.find_element_by_id("epdsubmit")
            cookieAccept.click()
        WebDriverWait(self.chrome, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_ctl00_ContentContainer_mainContent_ctl00_jobResultListNew"))
        )


    def nextPage(self):
        hasNextPage = bool(self.chrome.find_elements_by_link_text("Next"))
        if hasNextPage:
            nextButton = self.chrome.find_element_by_link_text("Next")
            nextButton.click()
            self.chrome.pageWait()
            return hasNextPage
        else:
            return False

    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()
        try:
            while True:
                jobContainers = self.chrome.find_elements_by_css_selector(".vsr-job")

                for jobContainer in jobContainers:
                    title = str(jobContainer.find_element_by_css_selector(".vsr-job__title").text)
                    title = title.strip()
                    self.job.setTitle(title)

                    link = jobContainer.find_element_by_css_selector(".vsr-job__title a").get_attribute("href")
                    link = link.strip()
                    self.job.setLink(link)

                    location = jobContainer.find_element_by_css_selector('div[data-id="div_content_VacV_LocationID"]').text
                    location = location.strip()
                    self.job.setLocation(location)

                    salary = jobContainer.find_element_by_css_selector('div[data-id="div_content_VacV_DisplaySalary"]').text
                    salary = salary.strip()
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
                elementToRemove = [self.chrome.find_element_by_css_selector("#ctl00_ctl00_ContentContainer_mainContent_lnkApply")]
                self.sanitizeElementsForDescription(elementToRemove)
                descriptionElement = self.chrome.find_element_by_id("ctl00_ctl00_ContentContainer_mainContent_fcVacancyDetailsDescription_ITSFields")
                description = descriptionElement.get_attribute('innerHTML')
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False

