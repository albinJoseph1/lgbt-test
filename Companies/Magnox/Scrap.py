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
        self.companyName = "Magnox"
        self.ownerUsername = "magnox"
        self.scrapPageURL = "https://careers.magnoxsites.com/vacancies.html#filter=p_web_site_id%3D6710%26p_published_to%3DWWW%26p_language%3DDEFAULT%26p_direct%3DY%26p_format%3DMOBILE%26p_include_exclude_from_list%3DN%26p_search%3D"
        self.feedType = self.feedTypeWebScrap
        self.maxScrapPageLimit = 20
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        WebDriverWait(self.chrome, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#main-content"))
        )
        self.chrome.pageWait()

    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()
        try:
            while True:
                jobContainers = self.chrome.find_elements_by_css_selector("div.jobCard")
                for jobContainer in jobContainers:
                    link = jobContainer.find_element_by_css_selector(".card-title a").get_attribute('href')
                    self.job.setLink(link)

                    title = jobContainer.find_element_by_css_selector(".card-title a").text
                    self.job.setTitle(title)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

                if self.nextPage():
                    pass
                else:
                    break

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                salary = self.chrome.find_element_by_id("salary_range").text.strip()
                self.jobs[currentJobIndex].setSalary(salary)

                location = self.chrome.find_element_by_id("work_location").text
                region = self.chrome.find_element_by_id("region").text
                location = location+", "+region
                self.jobs[currentJobIndex].setLocation(location)

                self.sanitizeElementsForDescription()

                description = self.chrome.find_element_by_css_selector("div.job_postings.job_detail").get_attribute('innerHTML')
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False

