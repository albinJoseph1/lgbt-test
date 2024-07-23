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
        self.companyName = "By Miles"
        self.ownerUsername = "bymiles"
        self.scrapPageURL = "https://careers.bymiles.co.uk/jobs"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.ID, "section-jobs"))
        )

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector("#section-jobs .block-grid li")
            for jobContainer in jobContainers:
                link = jobContainer.find_element_by_css_selector("a:first-child").get_attribute("href")
                self.job.setLink(link)

                title = jobContainer.find_element_by_css_selector("span.text-block-base-link").text
                self.job.setTitle(title)

                location = jobContainer.find_element_by_css_selector("a div:nth-child(2) div span:nth-child(3)").text
                self.job.setLocation(location)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                description = self.chrome.find_element_by_css_selector(".company-links div.font-company-body").get_attribute('innerHTML')
                self.jobs[currentJobIndex].setDescription(description)

                for i in range(10):
                    salary = self.chrome.find_element_by_css_selector(".company-links div:first-child p:nth-last-of-type(1)").text
                    if 'Salary' in salary:
                        salary = salary.split(":")[1]
                        self.jobs[currentJobIndex].setSalary(salary)
                        break
                    self.chrome.execute_script(""" jQuery(".company-links div:first-child p:nth-last-of-type(1)").remove() """)

            return True
        except:
            self.exceptionLogging()
            return False
