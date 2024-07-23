# Required Packages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
        self.companyName = "Gymshark"
        self.ownerUsername = "gymshark"
        self.scrapPageURL = "https://boards.eu.greenhouse.io/gymshark"
        self.feedType = self.feedTypeWebScrap
        self.jobTrackingVariableForLGBT = "t=c0ee1032teu"
        self.jobTrackingVariableForBME = "t=d2ff0a92teu"
        self.jobTrackingVariableForDISABILITY = "t=05e6c432teu"
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#main"))
        )

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector("#main div.opening")
            for jobContainer in jobContainers:
                title = str(jobContainer.find_element_by_css_selector("a").text)
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector("a").get_attribute("href")
                self.job.setLink(link, self.jobTrackingVariableForLGBT, lgbtManager.site.LGBT)
                self.job.setLink(link, self.jobTrackingVariableForBME, lgbtManager.site.BME)
                self.job.setLink(link, self.jobTrackingVariableForDISABILITY, lgbtManager.site.DISABILITY)

                location = str(jobContainer.find_element_by_css_selector(".location").text)
                self.job.setLocation(location)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                WebDriverWait(self.chrome, 50).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#app_body"))
                )

                self.sanitizeElementsForDescription()

                description = self.chrome.find_element_by_css_selector("#app_body #content").get_attribute('innerHTML')
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False
