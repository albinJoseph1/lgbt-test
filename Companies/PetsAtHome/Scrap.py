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
        self.companyName = "Pets At Home"
        self.ownerUsername = "petsathome"
        self.scrapPageURL = "https://www.petsathomejobs.com/search-jobs-and-apply"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        try:
            cookieButton = WebDriverWait(self.chrome, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#cookieOkButton"))
            )
            cookieButton.click()
        except Exception as e:
            pass

        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobGrid"))
        )

        while True:
            self.jobContainers = self.chrome.find_elements_by_css_selector(".jobGrid .job-box")

            self.chrome.clickElement(self.chrome.find_element_by_css_selector(".loadMoreJobs"))
            time.sleep(5)
            newContainers = self.chrome.find_elements_by_css_selector(".jobGrid .job-box")
            if len(self.jobContainers) == len(newContainers):
                break
            else:

                pass


    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()
        try:
            for jobContainer in self.jobContainers:
                title = str(jobContainer.find_element_by_css_selector("h4 > a").text)
                title = title.strip()
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector("h4 > a").get_attribute("href")
                self.job.setLink(link)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                value_containers = self.chrome.find_elements_by_css_selector("div.large-9.small-centered > div > p")
                for value_container in value_containers:
                    item_label = value_container.find_element_by_css_selector("strong").text
                    if 'Salary:' in item_label:
                        salary = value_container.text
                        salary = salary.split(":")[1].strip()
                        self.jobs[currentJobIndex].setSalary(salary)
                    if 'Location:' in item_label:
                        location = value_container.text
                        location = location.split(":")[1].strip()
                        self.jobs[currentJobIndex].setLocation(location)

                self.chrome.execute_script("""jQuery('div.large-9.small-centered > div > p').remove() """)
                description = self.chrome.find_element_by_css_selector("div.large-9.small-centered > div").get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False