# Required Packages
from Resource import htmlmin
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "PHS group"
        self.ownerUsername = "phsgroup"
        self.scrapPageURL = "https://careers.phs.co.uk/"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            ".departments"))
        )
        # searchBox.send_keys("All")
        # searchBox.send_keys(Keys.RETURN)
        #
        # WebDriverWait(self.chrome, 100).until(
        #     EC.presence_of_element_located((By.ID, "ctl00_ContentContainer_ctl00_VacancyListView"))
        # )
        # self.chrome.pageWait()

    def nextPage(self):
        try:
            next_button = self.chrome.find_element_by_css_selector('.paginator  > a:nth-last-child(2)')
        except:
            return False

        has_next_page = bool( self.chrome.find_elements_by_css_selector('.paginator  > a:last-child') )

        if has_next_page:
            next_button.click()
            time.sleep(3)
            WebDriverWait(self.chrome, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".paginator a"))
            )
            return has_next_page

        else:
            return False

        # Scraper Function

    def loadJobs(self):
        self.loadScrapPage()
        try:
            departmentLinks = []
            departments = self.chrome.find_elements_by_css_selector(".departments .grid__item--departments .tile__content--button a")
            for department in departments:
                departmentLink = department.get_attribute("href")
                departmentLinks.append(departmentLink)

            for departmentLink in departmentLinks:
                self.chrome.getComplete(departmentLink)
                while True:
                    hasCookie = bool(self.chrome.find_elements_by_css_selector(".cookiesDirective"))
                    if hasCookie:
                        CookieClose = self.chrome.find_element_by_css_selector(".cookiesDirective #epdsubmit").click()

                    jobContainers = self.chrome.find_elements_by_css_selector("#ctl00_ContentContainer_ctl00_pnVacancyResults .vsr-job")
                    for jobContainer in jobContainers:
                        title = str(jobContainer.find_element_by_css_selector(".vsr-job__title").text)
                        title = title.strip()
                        self.job.setTitle(title)

                        link = jobContainer.find_element_by_css_selector(".vsr-job__title a").get_attribute("href")
                        self.job.setLink(link)

                        location = jobContainer.find_element_by_css_selector("div[data-id = 'div_content_VacV_LocationID']").text
                        if location == "":
                            location = None
                        self.job.setLocation(location)

                        salary = jobContainer.find_element_by_css_selector("div[data-id = 'div_content_VacV_DisplaySalary']").text
                        salary = salary.replace('"',"")
                        self.job.setSalary(salary)

                        self.job.setCompanyName(self.companyName)
                        self.job.setOwnnerUsername(self.ownerUsername)

                        self.addToJobs()

                    if self.nextPage():
                        pass
                    else:
                        break

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                description = self.chrome.find_element_by_css_selector("#div_VacV_Description").get_attribute('innerHTML')

                self.jobs[currentJobIndex].setDescription(description)

            return True


        except:
            self.exceptionLogging()
            return False



