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
        self.companyName = "Maximus UK"
        self.ownerUsername = "maximusukserviceslimited"
        self.scrapPageURLs = ["https://chdaexternal-maximusuk.icims.com/jobs/search?ss=1&searchLocation=&searchCategory=&hashed=-435771476&mobile=false&width=1200&height=500&bga=true&needsRedirect=false&jan1offset=0&jun1offset=60","https://external-remploy-maximusuk.icims.com/jobs/search?ss=1&hashed=-435771476"]
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self, scrapPageURL):
        self.chrome.getComplete(scrapPageURL)
        try:
            cookieSection = WebDriverWait(self.chrome, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.cc-allow"))
            )
            cookieSection.click()
        except Exception as e:
            pass
        iframe = self.chrome.find_element_by_css_selector("#icims_content_iframe")
        self.chrome.switch_to.frame(iframe)
        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".iCIMS_ListingsPage"))
        )

    def nextPage(self):
        has_next_button = bool(self.chrome.find_element_by_css_selector('.iCIMS_MainWrapper .iCIMS_Paginator_Bottom .iCIMS_Paging > a:nth-last-child(2)').get_attribute("class")!="glyph invisible")
        if has_next_button:
            next_button = self.chrome.find_element_by_css_selector('.iCIMS_MainWrapper .iCIMS_Paginator_Bottom .iCIMS_Paging > a:nth-last-child(2)')
            self.chrome.clickElement(next_button)
            return has_next_button
        else:
            return False

    def loadJobs(self):
        try:
            for scrapPageURL in self.scrapPageURLs:
                self.loadScrapPage(scrapPageURL)

                while True:
                    self.chrome.pageWait()
                    jobContainers = self.chrome.find_elements_by_css_selector(".iCIMS_JobsTable .row")

                    for jobContainer in jobContainers:
                        title = jobContainer.find_element_by_css_selector(".title .iCIMS_Anchor h2").text
                        self.job.setTitle(title)

                        link = jobContainer.find_element_by_css_selector(".title .iCIMS_Anchor").get_attribute("href")
                        self.job.setLink(link)

                        location = jobContainer.find_element_by_css_selector(".header.left > span:last-child").text
                        self.job.setLocation(location)

                        salary_min = jobContainer.find_element_by_css_selector(".additionalFields dl.iCIMS_JobHeaderGroup >  div.iCIMS_JobHeaderTag:nth-child(2)").text.strip()
                        salary_min = salary_min.rstrip(salary_min[-1])
                        salary_min = salary_min.replace("Min", "").strip()
                        salary_max = jobContainer.find_element_by_css_selector(".additionalFields dl.iCIMS_JobHeaderGroup >  div.iCIMS_JobHeaderTag:last-child").text.strip()
                        salary_max = salary_max.rstrip(salary_max[-1])
                        salary_max = salary_max.replace("Max", "").strip()
                        if salary_min == salary_max:
                            salary = salary_min
                        else:
                            salary = salary_min + " - " + salary_max
                        salary = salary.replace("Select", "")
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

                iframe = self.chrome.find_element_by_css_selector("#icims_content_iframe")
                self.chrome.switch_to.frame(iframe)

                elementsTobeRemove = []
                elementsTobeRemoved = [".iCIMS_Logo",".iCIMS_PageFooter","#popupOverlay",".iCIMS_JobsTable"]
                for elementTobeRemoved in elementsTobeRemoved:
                    hasElementPresent = bool(self.chrome.find_elements_by_css_selector(elementTobeRemoved))
                    if hasElementPresent:
                        elementsTobeRemove.append(self.chrome.find_element_by_css_selector(elementTobeRemoved))
                self.sanitizeElementsForDescription(elementsTobeRemove)

                description = self.chrome.find_element_by_css_selector(".iCIMS_MainWrapper .iCIMS_JobContent").get_attribute('innerHTML')
                self.jobs[currentJobIndex].setDescription(description)

            return True
        except:
            self.exceptionLogging()
            return False
