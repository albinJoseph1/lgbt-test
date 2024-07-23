# Required Packages
from Resource import htmlmin
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Companies.StandardAgent import ScrapAgent
from Managers import lgbtManager


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Peerpoint"
        self.ownerUsername = "peerpoint"
        self.scrapPageURL = "https://krb-sjobs.brassring.com/TGnewUI/Search/Home/HomeWithPreLoad?partnerid=30147&siteid=5040&PageType=searchResults&SearchType=linkquery&LinkID=6#keyWordSearch=&locationSearch="
        self.feedType = self.feedTypeWebScrap
        self.jobTrackingVariableForLGBT = "codes=lgbtjobs"
        self.jobTrackingVariableForBME = "codes=bmejobs"
        self.jobTrackingVariableForDISABILITY = "codes=disabilityjob"
        self.location = "London - Bishops Square"
        self.maxScrapPageLimit = 20
        self.agentQueuePriority = 100
        self.waitingTimeMultiplier = 2
        #     Company Details End


    def loadScrapPage(self):
         self.chrome.getComplete(self.scrapPageURL, True)

    def nextPage(self):

        has_next_page = bool(self.chrome.find_elements_by_css_selector("#showMoreJobs"))
        if has_next_page:
            next_button = self.chrome.find_element_by_css_selector("#showMoreJobs")
            next_button.click()
            time.sleep(3 * self.waitingTimeMultiplier)
            return has_next_page
        else:
            return False

    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()
        try:
            self.chrome.find_element_by_css_selector(".powerSearchLink a").click()
            self.chrome.pageWait()
            self.chrome.find_element_by_css_selector("input[name = 'powerSearchLocationSearch']").send_keys("London")
            checkBoxes = self.chrome.find_elements_by_css_selector(".checkboxLabel")
            for checkBox in checkBoxes:
                checkBoxText = checkBox.text
                if checkBoxText == "Peerpoint":
                    checkBox.click()
            self.chrome.find_element_by_css_selector(".bottomControlWrapper .bottomControl").click()

            while True:
                time.sleep(5 * self.waitingTimeMultiplier)
                jobsOuter = WebDriverWait(self.chrome, 20 * self.waitingTimeMultiplier).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#mainJobListContainer"))
                )
                jobContainers = jobsOuter.find_elements_by_css_selector(".jobList .job.ng-scope")

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


                jobsDetail = WebDriverWait(self.chrome, 20 * self.waitingTimeMultiplier).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".mainDetails"))
                )

                self.sanitizeElementsForDescription()

                jobDescription = jobsDetail.find_element_by_css_selector(
                    ".answer.jobdescriptionInJobDetails").get_attribute(
                    "innerHTML")
                self.jobs[currentJobIndex].setDescription(jobDescription)

            return True

        except:
            self.exceptionLogging()
            return False

