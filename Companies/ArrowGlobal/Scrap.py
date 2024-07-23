# Required Packages
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
        self.companyName = "Arrow Global"
        self.ownerUsername = "arrowglobal"
        self.scrapPageURL = "https://arrowglobal.current-vacancies.com/Careers/Arrow-Global-External-VSP-3269"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "#results .vacancy-search-result-item"))
        )

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector("#results .vacancy-search-result-item")
            for jobContainer in jobContainers:
                title = str(jobContainer.find_element_by_css_selector("[data-bind='VacancyTitle']").text)
                title = title.strip()
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector("[data-bind='ApplyLink']").get_attribute("href")
                self.job.setLink(link)

                location = jobContainer.find_element_by_css_selector("[data-bind='Location']").text
                self.job.setLocation(location)

                salary = jobContainer.find_element_by_css_selector("[data-bind='Salary']").text
                self.job.setSalary(salary, "£?(\d+(?:,?|\.)\d+)\s*-\s*£?(\d+(?:,?|\.)\d+)",is_salary_text=True)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                description = self.chrome.find_element_by_css_selector("#top #GlobalContent_HeaderTitle1 + div .PLACEHOLDER div").get_attribute('innerHTML')
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False