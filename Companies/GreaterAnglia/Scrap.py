# Required Packages
from datetime import datetime
import datetime
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
        self.companyName = "Greater Anglia"
        self.ownerUsername = "greateranglia"
        self.scrapPageURL = "https://careers.greateranglia.co.uk/vacancies"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):

        # self.chrome.getComplete('https://proxyscrape.com/web-proxy')
        # searchField = self.chrome.find_element_by_name("url")
        # searchField.send_keys("https://careers.greateranglia.co.uk/vacancies")
        # searchField.submit()

        self.chrome.getComplete(self.scrapPageURL)
        cookieCloseButton = WebDriverWait(self.chrome, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
        )
        cookieCloseButton.click()

        WebDriverWait(self.chrome, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".vacancy-wrapper .job-department > a"))
        )

    # Scraper Function
    def loadJobs(self):

        self.loadScrapPage()

        try:

            categoryContainers = self.chrome.find_elements_by_css_selector(".vacancy-wrapper .job-department a")
            categoryLinks = []
            for categoryContainer in categoryContainers:
                categoryLinks.append(categoryContainer.get_attribute("href"))

            for categoryLink in categoryLinks:

                # self.chrome.getComplete('https://proxyscrape.com/web-proxy')
                # searchField = self.chrome.find_element_by_name("url")
                # searchField.send_keys(categoryLink)
                # searchField.submit()

                self.chrome.getComplete(categoryLink)
                self.chrome.pageWait()
                WebDriverWait(self.chrome, 50).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".vacancy-wrapper.visible .row"))
                )
                jobContainers = self.chrome.find_elements_by_css_selector(".vacancy-wrapper.visible .row")
                for jobContainer in jobContainers:
                    title = str(jobContainer.find_element_by_css_selector("span.job-title").text)
                    title = title.strip()
                    self.job.setTitle(title)

                    # try:
                    #     location = str(jobContainer.find_element_by_css_selector(".job-location").text)
                    #     location = location.strip()
                    #     self.job.setLocation(location)
                    # except Exception as e:
                    #     exception_message = str(title) + ' : ' + str(e) + "\n"
                    #     print(exception_message)
                    #     self.exceptionLogging('warning', exception_message)


                    salary = str(jobContainer.find_element_by_css_selector("span.job-salary").text)
                    salary = salary.replace("Salary:", "")
                    salary = salary.strip()
                    self.job.setSalary(salary)

                    link = jobContainer.find_element_by_css_selector("a.view-more-btn").get_attribute("href")
                    self.job.setLink(link)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)
                    self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):

                self.chrome.getComplete(job.getLink())
                self.chrome.pageWait()

                try:
                    location = str(self.chrome.find_element_by_css_selector(".vacancy-description-left .value_location").text)
                    location = location.strip()
                    self.jobs[currentJobIndex].setLocation(location)
                except Exception as e:
                    exception_message = str(job.getTitle()) + ' : ' + str(e) + "\n"
                    self.exceptionLogging('warning', exception_message)

                contract = self.chrome.find_element_by_css_selector(".vacancy-description-left .value_type_of_role").text
                contract = contract.strip()
                self.jobs[currentJobIndex].setContract(contract)

                expire = self.chrome.find_element_by_css_selector(".vacancy-description-left .value_closing_date").text
                expire = expire.strip()
                try:
                    expire = datetime.datetime.strptime(expire, '%d/%m/%Y').strftime('%Y-%m-%d')
                    self.jobs[currentJobIndex].setExpireDate(expire)
                except Exception as e:
                    exception_message = str(job.getTitle()) + ' : ' + str(e) + "\n"
                    self.exceptionLogging('warning', exception_message)

                self.sanitizeElementsForDescription()
                descriptionElement = self.chrome.find_element_by_css_selector('.job-content')
                description = descriptionElement.get_attribute('innerHTML')
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False

