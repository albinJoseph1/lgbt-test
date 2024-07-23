# Required Packages
import time

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
        self.companyName = "Allsaints"
        self.ownerUsername = "allSaints"
        self.scrapPageURL = "https://careers.allsaints.com/job-search"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-container"))
        )
        self.chrome.clickElement(self.chrome.find_element_by_css_selector(".button-for-region"))
        time.sleep(3)
        self.chrome.clickElement(
            self.chrome.find_element_by_css_selector("#filter-content-regions .region label:first-child"))
        time.sleep(3)
        self.chrome.clickElement(self.chrome.find_element_by_css_selector("#apply-region"))
        self.chrome.pageWait()

        while True:
            self.jobContainers = self.chrome.find_elements_by_css_selector(".jobs-container .job")

            self.chrome.clickElement(self.chrome.find_element_by_css_selector("#load-more"))
            time.sleep(5)
            newContainers = self.chrome.find_elements_by_css_selector(".jobs-container .job")
            if len(self.jobContainers) == len(newContainers):
                break
            else:

                pass


    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()
        try:

            for jobContainer in self.jobContainers:
                title = str(jobContainer.find_element_by_css_selector(".job-title").text)
                title = title.strip()
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector("a.line-link").get_attribute("href")
                self.job.setLink(link)

                location = jobContainer.find_element_by_css_selector(".job-details").text.split(",")[0]
                self.job.setLocation(location)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                description = self.chrome.find_element_by_css_selector("#job-detail .job-wrapper").get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)

            return True


        except:
            self.exceptionLogging()
            return False