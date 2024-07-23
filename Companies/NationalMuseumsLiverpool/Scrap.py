# Required Packages
from Resource import htmlmin
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
        self.companyName = "National Museums Liverpool"
        self.ownerUsername = "nationalmuseumsliverpool"
        self.scrapPageURL = "https://www.liverpoolmuseums.org.uk/jobs"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".page-transition-enter-done .fade-enter-done"))
        )

    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobOuterIndex = 1
            jobContainers = self.chrome.find_elements_by_css_selector(".page-transition-enter-done .section__body h3")
            for jobContainer in jobContainers:
                title = str(jobContainer.text)
                title = title.strip()
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector("a").get_attribute("href")
                self.job.setLink(link)

                salary = self.chrome.find_element_by_css_selector(".page-transition-enter-done .section__body h3:nth-of-type("+str(jobOuterIndex)+") + p").text
                salary = salary.split(":")
                salary = salary[1]
                self.job.setSalary(salary)

                hasExpireDate = bool(self.chrome.find_elements_by_css_selector(".page-transition-enter-done .section__body h3:nth-of-type("+str(jobOuterIndex)+") + p + p"))
                if hasExpireDate:
                    expireDate = self.chrome.find_element_by_css_selector(".page-transition-enter-done .section__body h3:nth-of-type("+str(jobOuterIndex)+") + p + p").text
                    expireDate = expireDate.split(":")
                    expireDate = expireDate[1].strip()
                    try:
                        expireDate = datetime.strptime(expireDate,'%d/%m/%Y %H')
                        expireDate = expireDate.strftime('%Y-%m-%d')
                        self.job.setExpireDate(expireDate)
                    except Exception as e:
                        exception_message = str(title) + ' : ' + str(e) + "\n"
                        self.exceptionLogging('warning', exception_message)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

                jobOuterIndex = int(jobOuterIndex) + 1

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                WebDriverWait(self.chrome, 100).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".AdvertParentContainer div:nth-child(5) p:first-child"))
                )

                location = self.chrome.find_element_by_css_selector(".AdvertParentContainer div:nth-child(5) p:first-child").text
                location = location.split(":")
                location = location[1].strip()
                self.jobs[currentJobIndex].setLocation(location)

                contract = self.chrome.find_element_by_css_selector(".AdvertParentContainer div:nth-child(5) p:nth-of-type(3)").text
                contract = contract.split(":")
                contract = contract[1].strip()
                self.jobs[currentJobIndex].setContract(contract)

                self.sanitizeElementsForDescription()

                description = self.chrome.find_element_by_css_selector(".AdvertParentContainer div:nth-child(11)").get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)

            return True
        except:
            self.exceptionLogging()
            return False