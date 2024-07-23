# Required Packages
import time
from datetime import datetime
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
        self.companyName = "Orbit"
        self.ownerUsername = "orbit"
        self.scrapPageURL = "https://www.orbitgroup.org.uk/careers/current-vacancies/"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        try:
            cookieCloseButton = WebDriverWait(self.chrome, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#ccc-notify-accept"))
            )
            cookieCloseButton.click()
        except Exception as e:
            exception_message = str(e) + "\n"
            self.exceptionLogging('warning', exception_message)

        try:
            WebDriverWait(self.chrome, 50).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#loadThis"))
            )
        except:
            WebDriverWait(self.chrome, 50).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#vacancies-jobs-wrapper .job-card"))
            )

    def loadMoreJobs(self):

        while True:
            time.sleep(7)
            has_load_more_button = bool(
                self.chrome.find_element_by_css_selector("#VF_vacancies #loadThis").get_attribute(
                    "style") != "display: none;")
            if has_load_more_button:
                load_more_button = self.chrome.find_element_by_css_selector("#VF_vacancies #loadThis")
                self.chrome.clickElement(load_more_button)
                pass
            else:
                break

        try:
            WebDriverWait(self.chrome, 500).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#loadThis.VF_item_disabled"))
            )
        except:
            WebDriverWait(self.chrome, 500).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#vacancies-jobs-wrapper .job-card"))
            )
        pass

    def loadJobs(self):
        self.loadScrapPage()
        try:
            self.loadMoreJobs()
            jobContainers = self.chrome.find_elements_by_css_selector("#vacancies-jobs-wrapper .job-card")
            for jobContainer in jobContainers:
                title = jobContainer.find_element_by_css_selector(".job-title").text
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector(".content > a:first-child").get_attribute("href")
                self.job.setLink(link)

                location = jobContainer.find_element_by_css_selector(".job-location").text
                self.job.setLocation(location)

                salary = jobContainer.find_element_by_css_selector(".job-salary").text
                self.job.setSalary(salary)

                contract = jobContainer.find_element_by_css_selector(".job-type").text
                self.job.setContract(contract)

                expireDate = jobContainer.find_element_by_css_selector(".job-closing-date").text
                possibleExpiryDateFormats = [
                    "%d %B %Y",
                    "%d %B %Y %Ham",
                    "%d %B %Y %Hpm",
                    "%d/%m/%Y",
                    "%a, %d %b %Y"
                ]

                formattedExpireDate = None
                for expiryDateFormat in possibleExpiryDateFormats:
                    try:
                        formattedExpireDate = datetime.strptime(expireDate, expiryDateFormat).strftime('%Y-%m-%d')
                        break
                    except:
                        pass

                if formattedExpireDate is None:
                    exception_message = str(title) + ' : Unknown expiry date format ' + expireDate + "\n"
                    self.exceptionLogging('warning', exception_message)
                else:
                    self.job.setExpireDate(formattedExpireDate)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                description = self.chrome.find_element_by_css_selector(".careersdetail-content").get_attribute(
                    "innerHTML")
                self.jobs[currentJobIndex].setDescription(description)

            return True
        except:
            self.exceptionLogging()
            return False