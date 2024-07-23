# Required Packages
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
        self.companyName = "Royal College of Psychiatrists"
        self.ownerUsername = "royalcollegeofpsychiatrists"
        self.scrapPageURL = "https://www.rcpsych.ac.uk/about-us/work-for-us/vacancies-at-the-college"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector(".container ul.jobs-list >li")
            for jobContainer in jobContainers:
                title = str(jobContainer.find_element_by_css_selector("h3").text.strip())
                self.job.setTitle(title)

                job_nav_elements = jobContainer.find_elements_by_css_selector('ul.job-nav li')
                location = None
                salary = None
                for element in job_nav_elements:
                    text = element.text
                    if "location" in text.lower():
                        location = text.split(":")[1].strip()
                        self.job.setLocation(location)
                    elif "salary" in text.lower():
                        salary = text.split(":")[1].strip()
                        self.job.setSalary(salary, "£?(\d+(?:,?|\.)\d+)\s*-\s*£?(\d+(?:,?|\.)\d+)|(\d+)", is_salary_text=True)

                link = jobContainer.find_element_by_css_selector("a.button-link").get_attribute("href")
                self.job.setLink(link)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()
                description = self.chrome.find_element_by_xpath('//div[@class="events-section vacancies-section"]//div[not(@class) and not(@id)][1]').get_attribute('innerHTML')
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False
