# Required Packages
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
        self.companyName = "Magenta Living"
        self.ownerUsername = "magentaliving"
        self.location = "Birkenhead"
        self.scrapPageURL = "https://www.jobtrain.co.uk/magentalivingjobs/vacancies_v3.aspx"
        self.feedType = self.feedTypeWebScrap
        self.maxScrapPageLimit = 20
        self.additionalFetch = True

        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        WebDriverWait(self.chrome, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".JT-column .JT-nine.JT-column.JT-last.JT-pt"))
        )

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector(".JT-ui.JT-card")
            for jobContainer in jobContainers:
                title = jobContainer.find_element_by_css_selector(".JT-content a.JT-header").text
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector(".JT-content a.JT-header").get_attribute('href')
                self.job.setLink(link)

                self.job.setLocation(self.location)
                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())
                WebDriverWait(self.chrome, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".JT-column"))
                )

                elementsToRemove = []
                applyButtons = self.chrome.find_elements_by_css_selector("a")
                for applyButton in applyButtons:
                    elementsToRemove.append(applyButton)
                self.sanitizeElementsForDescription(elementsToRemove)

                salary = self.chrome.find_element_by_css_selector(".JT-four .salary").text
                salary = salary.split(":")[1].strip()
                contract = self.chrome.find_element_by_css_selector(".JT-four .division").text
                contract = contract.split(":")[1].strip()
                description = self.chrome.find_element_by_css_selector(".JT-container").get_attribute("innerHTML")

                self.jobs[currentJobIndex].setSalary(salary)
                self.jobs[currentJobIndex].setContract(contract)
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False
