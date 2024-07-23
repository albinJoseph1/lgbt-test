# Required Packages
from Resource import htmlmin
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
        self.companyName = "Personal Group"
        self.ownerUsername = "personalgroup"
        self.scrapPageURL = "https://www.personalgroupcareers.com/jobs"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".jobs-list-container"))
        )

    def loadJobs(self):

        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector(
                "div.jobs-list-container ul[id='jobs_list_container'] li.w-full")
            for jobContainer in jobContainers:
                title = jobContainer.find_element_by_css_selector(
                    "a span[title]").text.strip()
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector(
                    "a").get_attribute("href")
                self.job.setLink(link)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                WebDriverWait(self.chrome, 100).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "section.company-links"))
                )

                self.sanitizeElementsForDescription()

                jobDescription = self.chrome.find_element_by_css_selector(
                    "section.company-links div.font-company-body").get_attribute("outerHTML")
                self.jobs[currentJobIndex].setDescription(
                    htmlmin.minify(jobDescription))

                hasJobDetails = bool(self.chrome.find_elements_by_css_selector(
                    "section.pb-20 dl.company-links"))
                if hasJobDetails:
                    jobDetailLabels = self.chrome.find_elements_by_css_selector(
                        "section.pb-20 dl.company-links dt")
                    for label in jobDetailLabels:
                        if 'Locations' in label.text:
                            location = label.find_element_by_xpath(
                                "following-sibling::dd").text.strip()
                            self.jobs[currentJobIndex].setLocation(location)
                        if 'Yearly salary' in label.text:
                            salary = label.find_element_by_xpath(
                                "following-sibling::dd").text.strip()
                            self.jobs[currentJobIndex].setSalary(
                                salary, "£?(\d+(?:,?|\.)\d+)\s*-\s*£?(\d+(?:,?|\.)\d+)|£?(\d+(?:,?|\.)\d+)", is_salary_text=True)
                        if 'Employment type' in label.text:
                            contractType = label.find_element_by_xpath(
                                "following-sibling::dd").text.strip()
                            self.jobs[currentJobIndex].setContract(
                                contractType)
            return True
        except:
            self.exceptionLogging()
            return False
