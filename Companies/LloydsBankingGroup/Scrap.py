# Required Packages
from datetime import datetime
from Resource import htmlmin
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Managers import lgbtManager
from Objects import Job

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Lloyds Banking Group"
        self.ownerUsername = "lloydsbankinggroup"
        self.scrapPageURL = 'https://lbg.wd3.myworkdayjobs.com/lbg_Careers'
        self.jobTrackingVariableForLGBT = "source=lgbt-jobs"
        self.jobTrackingVariableForBME = "source=bmejobs"
        self.jobTrackingVariableForDISABILITY = "source=disability-job"

        self.feedType = self.feedTypeWebScrap
        self.maxScrapPageLimit = 20
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        try:
            cookieSection = WebDriverWait(self.chrome, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-automation-id='legalNoticeAcceptButton']"))
            )
            cookieSection.click()
        except Exception as e:
            exception_message = str(e) + "\n"
            self.exceptionLogging('warning', exception_message)

        WebDriverWait(self.chrome, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainContent"))
        )


    def nextPage(self):
        # self.chrome.switch_to_frame(0)

        has_next_page = bool(self.chrome.find_elements_by_css_selector('nav[aria-label="pagination"] button[aria-label="next"]'))
        if has_next_page:
            next_button = self.chrome.find_element_by_css_selector('nav[aria-label="pagination"] button[aria-label="next"]')
            next_button.click()
            WebDriverWait(self.chrome, 50).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "ul[role='list']"))
            )
            time.sleep(5)
            return has_next_page
        else:
            return False

    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()

        try:
            while True:
                jobContainers = self.chrome.find_elements_by_css_selector("ul[role='list'] li.css-1q2dra3")
                for jobContainer in jobContainers:
                    try:
                        title = str(jobContainer.find_element_by_css_selector('a[data-automation-id="jobTitle"]').text.strip())
                        self.job.setTitle(title)
                        link = jobContainer.find_element_by_css_selector(
                            "a[data-automation-id='jobTitle']").get_attribute(
                            'href')
                        self.job.setLink(link, self.jobTrackingVariableForLGBT, lgbtManager.site.LGBT)
                        self.job.setLink(link, self.jobTrackingVariableForBME, lgbtManager.site.BME)
                        self.job.setLink(link, self.jobTrackingVariableForDISABILITY, lgbtManager.site.DISABILITY)

                    except Exception as e:
                        exception_message = self.scrapPageURL + ":" + str(e) + "\n"
                        self.exceptionLogging('warning', exception_message)
                        continue

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)
                    self.addToJobs()
                    print(self.job.getLink())

                if self.nextPage():
                    pass
                else:
                    break

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())
                self.chrome.pageWait()
                try:
                    WebDriverWait(self.chrome, 50).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, 'div[data-automation-id="jobPostingPage"]'))
                    )
                except Exception as e:
                    exception_message = str(job.getTitle()) + ' : ' + str(e) + "\n"
                    self.exceptionLogging('warning', exception_message)
                    continue
                try:
                    location = str(self.chrome.find_element_by_css_selector(
                        'div[data-automation-id="jobPostingPage"] div[data-automation-id="locations"] dl').text)
                    location = location.replace("locations\n", "")
                    location = location.replace("\n", ", ")
                    location = location.strip()
                    self.jobs[currentJobIndex].setLocation(location)
                except Exception as e:
                    exception_message = str(job.getTitle()) + ' : ' + str(e) + "\n"
                    self.exceptionLogging('warning', exception_message)

                self.sanitizeElementsForDescription()
                try:
                    description = self.chrome.find_element_by_css_selector( '#mainContent div[data-automation-id="jobPostingDescription"]').get_attribute(
                        'innerHTML')
                    description = description.replace('\n', '')
                    description = description.replace('\u00a3', '&#163;')
                    self.jobs[currentJobIndex].setDescription(description)
                except Exception as e:
                    exception_message = str(job.getTitle()) + ' : ' + str(e) + "\n"
                    self.exceptionLogging('warning', exception_message)

            return True

        except:
            self.exceptionLogging()
            return False

