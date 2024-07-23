# Required Packages
from datetime import datetime
from Resource import htmlmin
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage=None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Computershare"
        self.ownerUsername = "computershare"
        self.scrapPageURL = "https://fa-evdq-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/computersharecareers/requisitions?location=United+Kingdom&locationId=300000000473193&locationLevel=country&mode=location"
        self.feedType = self.feedTypeWebScrap
        self.agentQueuePriority = 101
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        hasCookieSection = bool(self.chrome.find_elements_by_css_selector(
            ".cookie-consent__content .cookie-consent__actions button.accept"))
        if hasCookieSection:
            cookieSection = self.chrome.find_element_by_css_selector(
                ".cookie-consent__content .cookie-consent__actions button.accept")
            cookieSection.click()

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".search-job-results"))
        )

    def loadJobs(self):

        self.loadScrapPage()

        try:
            initial_job_count = 0
            while True:
                self.chrome.scrollToBottom()
                time.sleep(6)
                jobContainers = self.chrome.find_elements_by_css_selector(
                    ".search-results-jobs-list ul.jobs-list__list li[data-qa='searchResultItem']")
                total_job_count = len(jobContainers)
                if initial_job_count == total_job_count:
                    break
                elif initial_job_count < total_job_count:
                    initial_job_count = total_job_count
                    continue
                else:
                    self.exceptionLogging(
                        "error", exception_message="Unable to scrape all jobs within the given time limit")
                    return False
            for jobContainer in jobContainers:
                link = jobContainer.find_element_by_css_selector(
                    ".job-tile .job-list-item__link").get_attribute('href')
                self.job.setLink(link)

                title = jobContainer.find_element_by_css_selector(
                    ".job-tile .job-tile__title").text.strip()
                self.job.setTitle(title)

                location = jobContainer.find_element_by_css_selector(
                    ".job-tile__subheader span[data-bind='html: primaryLocation']").get_attribute("innerHTML")
                self.job.setLocation(location)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                retries = 5
                for attempt in range(retries):
                    try:
                        self.chrome.getComplete(job.getLink())
                        WebDriverWait(self.chrome, 100).until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, ".job-details__section"))
                        )
                        break

                    except WebDriverException as e:
                        if attempt < retries - 1:
                            self.exceptionLogging(
                                "error", exception_message=f"Retrying...{attempt + 1}")
                            time.sleep(5)
                        else:
                            self.exceptionLogging(
                                "error", exception_message=f"Failed to load job details page after {retries} retries")
                            self.jobs.pop(currentJobIndex)
                            continue

                jobDetails = self.chrome.find_elements_by_css_selector("div.job-details__section")
                self.sanitizeElementsForDescription()
                description = ''
                for jobDetail in jobDetails:
                    try:
                        jobDetailTitle = jobDetail.find_element_by_css_selector(
                            "div.job-details__section .job-details__description-header").text
                    except:
                        jobDetailTitle = None
                    if jobDetailTitle:
                        if jobDetailTitle == 'JOB DESCRIPTION':
                            description = jobDetail.find_element_by_css_selector(
                                "div.job-details__section .job-details__description-content").get_attribute('innerHTML')
                        elif jobDetailTitle == 'ABOUT US':
                            aboutUs = jobDetail.get_attribute('innerHTML')
                            description = description + aboutUs
                        elif jobDetailTitle == 'ABOUT THE TEAM':
                            aboutTheTeam = jobDetail.get_attribute('innerHTML')
                            description = description + aboutTheTeam
                        elif jobDetailTitle == 'JOB INFO':
                            jobInfoList = jobDetail.find_elements_by_css_selector(
                                ".job-details__info-section ul.job-meta__list li.job-meta__item")
                            for jobInfo in jobInfoList:
                                jobInfoTitle = jobInfo.find_element_by_css_selector(
                                    ".job-meta__title").text
                                jobInfoValue = jobInfo.find_element_by_css_selector(
                                    ".job-meta__subitem").text
                                if jobInfoTitle == 'Apply Before':
                                    expireDate = jobInfoValue
                                    expireDate = datetime.strptime(expireDate, '%m/%d/%Y, %I:%M %p').strftime('%Y-%m-%d')
                                    self.jobs[currentJobIndex].setExpireDate(
                                        expireDate)
                                elif jobInfoTitle == 'Job Schedule':
                                    jobContract = jobInfoValue.strip()
                                    self.jobs[currentJobIndex].setContract(
                                        jobContract)
                    else:
                        continue

                self.jobs[currentJobIndex].setDescription(description)

            return True
        except:
            self.exceptionLogging()
            return False
