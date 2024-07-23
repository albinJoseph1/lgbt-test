# Required Packages
import time
from datetime import datetime
import datetime
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
        self.companyName = "Pinsent Masons"
        self.ownerUsername = "pinsentmasons"
        self.scrapPageURL = "https://ehpy.fa.em5.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/requisitions?location=United+Kingdom&locationId=300000000228702&locationLevel=country&mode=location"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".search-job-results"))
        )

    def loadJobs(self):
        self.loadScrapPage()
        try:
            self.chrome.execute_script("""jQuery('li[data-qa="searchResultTalentCommunityItem"]').remove()""")
            total_job_count = int(self.chrome.find_element_by_css_selector(".search-filters__sections .search-filters__counter").get_attribute("innerHTML").split(" ")[0].strip())
            initial_time = datetime.datetime.now().minute
            while True:
                self.chrome.scrollToBottom()
                time.sleep(1)
                jobContainers = self.chrome.find_elements_by_css_selector(".search-results-jobs-list li[data-qa='searchResultItem']")
                job_count = len(jobContainers)
                current_time = datetime.datetime.now().minute
                if job_count == total_job_count:
                    break
                elif ((current_time - initial_time) % 60) > 5:
                    self.exceptionLogging("error", exception_message="Unable to scrape all jobs within the given time limit")
                    return False
                else:
                    continue

            for jobContainer in jobContainers:
                link = jobContainer.find_element_by_css_selector(".job-tile .job-grid-item__link").get_attribute('href')
                self.job.setLink(link)

                title = jobContainer.find_element_by_css_selector(".job-grid-item__link .job-tile__title").text
                self.job.setTitle(title)

                location = jobContainer.find_element_by_css_selector(".job-tile__subheader span[data-bind='html: primaryLocation']").get_attribute("innerHTML")
                location = location.split(",")[0].strip()
                self.job.setLocation(location)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()
                try:
                    description = self.chrome.find_element_by_css_selector(".job-details__section > div.job-details__description-content").get_attribute('innerHTML')
                    self.jobs[currentJobIndex].setDescription(description)
                except:
                    self.exceptionLogging("warning", exception_message="Unable to scrap description, skipping job "+job.getLink())

            return True
        except:
            self.exceptionLogging()
            return False
