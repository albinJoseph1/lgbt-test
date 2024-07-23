# Required Packages
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
        self.companyName = "Accent Group"
        self.ownerUsername = "accentgroup"
        self.scrapPageURL = "https://isw.changeworknow.co.uk/accent_group/vms/e/careers/search/new?utm_campaign=Accent-Careers&utm_medium=website"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):

        self.chrome.getComplete(self.scrapPageURL)
        cookieSection = WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.cnl-cookie-accept.btn.btn-primary"))
        )
        cookieSection.click()

        self.chrome.pageWait()
        WebDriverWait(self.chrome, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".panel-body .position_opening"))
        )

    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()

        try:
            jobContainers = self.chrome.find_elements_by_css_selector(".position_opening")
            for jobContainer in jobContainers:
                title = str(jobContainer.find_element_by_css_selector("h1.panel-title > a").text)
                title = title.strip()
                self.job.setTitle(title)

                location = str(jobContainer.find_element_by_css_selector(".panel-body > p:first-child").text)
                location = location.replace("Location:", "")
                location = location.strip()
                self.job.setLocation(location)

                contract = str(jobContainer.find_element_by_css_selector(".panel-body > p:nth-child(2)").text)
                contract = contract.replace("Contract Type:", "")
                contract = contract.strip()
                self.job.setContract(contract)

                expire = str(jobContainer.find_element_by_css_selector(".panel-body > p:last-child").text)
                expire = expire.replace("Closing Date:", "")
                expire = expire.strip()

                try:
                    expire = datetime.datetime.strptime(expire, '%d %B %Y').strftime('%Y-%m-%d')
                    self.job.setExpireDate(expire)
                except Exception as e:
                    exception_message = str(title) + ' : ' + str(e) + "\n"
                    self.exceptionLogging('warning', exception_message)

                link = jobContainer.find_element_by_css_selector("h1.panel-title > a").get_attribute("href")
                self.job.setLink(link)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()



            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())
                self.chrome.pageWait()

                for i in range(1):
                    self.chrome.execute_script("""
                                                   jQuery("#position_display .panel-default .panel-body > div > p:nth-child(1)").remove();
                                               """)

                self.sanitizeElementsForDescription()

                descriptionElement = self.chrome.find_element_by_xpath('//*[@id="position_display"]/div/div/div[3]')
                description = descriptionElement.get_attribute('innerHTML')

                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False

