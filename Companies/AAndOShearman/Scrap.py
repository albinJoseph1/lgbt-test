# Required Packages
from Resource import htmlmin
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Managers import lgbtManager

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "A&O Shearman"
        self.ownerUsername = "allenovery"
        self.location = "London - Bishops Square"
        self.scrapPageURL = "https://krb-sjobs.brassring.com/TGnewUI/Search/Home/HomeWithPreLoad?partnerid=30147&siteid=5040&PageType=searchResults&SearchType=linkquery&LinkID=6#keyWordSearch=&locationSearch="
        self.feedType = self.feedTypeWebScrap
        self.jobTrackingVariableForLGBT = "codes=lgbtjobs"
        self.jobTrackingVariableForBME = "codes=bmejobs"
        self.jobTrackingVariableForDISABILITY = "codes=disabilityjob"
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL, True)
        WebDriverWait(self.chrome, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".powerSearchLink a"))
        )

    def nextPage(self):
        has_next_page = bool(self.chrome.find_elements_by_css_selector("#showMoreJobs"))
        if has_next_page:
            next_button = self.chrome.find_element_by_css_selector("#showMoreJobs")
            next_button.click()
            self.chrome.pageWait()
            WebDriverWait(self.chrome, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#mainJobListContainer"))
            )
            return has_next_page
        else:
            return False

    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()

        try:
            self.chrome.find_element_by_css_selector(".powerSearchLink a").click()
            self.chrome.pageWait()
            input_key = WebDriverWait(self.chrome, 25).until(
                            EC.presence_of_element_located((By.NAME, "powerSearchLocationSearch"))
                        )
            input_key.send_keys("London")
            checkBoxes = WebDriverWait(self.chrome, 35).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".checkboxLabel"))
                        )
            for checkBox in checkBoxes:
                checkBoxText = checkBox.text
                if checkBoxText == "Experienced Hire & Support":
                    checkBox.click()
            self.chrome.find_element_by_css_selector(".bottomControlWrapper .bottomControl").click()

            while True:
                time.sleep(5)
                self.chrome.execute_script("""jQuery('.jobList .job.no-items').remove()""")
                jobsOuter = WebDriverWait(self.chrome, 100).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#mainJobListContainer"))
                )
                jobContainers = jobsOuter.find_elements_by_css_selector(".jobList .job")
                for jobContainer in jobContainers:
                    title = jobContainer.find_element_by_css_selector(".jobProperty.jobtitle").get_attribute('text')
                    self.job.setTitle(title)
                    link = jobContainer.find_element_by_css_selector(".jobProperty.jobtitle").get_attribute('href')
                    self.job.setLink(link, self.jobTrackingVariableForLGBT, lgbtManager.site.LGBT)
                    self.job.setLink(link, self.jobTrackingVariableForBME, lgbtManager.site.BME)
                    self.job.setLink(link, self.jobTrackingVariableForDISABILITY, lgbtManager.site.DISABILITY)

                    self.job.setLocation(self.location)
                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

                if self.nextPage():
                    pass
                else:
                    break

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                jobsDetail = WebDriverWait(self.chrome, 100).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".mainDetails"))
                )

                self.sanitizeElementsForDescription()

                description = jobsDetail.find_element_by_css_selector(
                    ".answer.jobdescriptionInJobDetails").get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)


            return True

        except:
            self.exceptionLogging()
            return False

