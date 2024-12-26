# Required Packages
from Resource import htmlmin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Aviva"
        self.ownerUsername = "aviva"
        self.scrapPageURL = "https://careers.aviva.co.uk/apply/?perPage=999&page=1"
        self.jobTrackingVariable = "source=Aviva_Rec_LGBTjobs"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        hasCookieSection = self.chrome.find_elements_by_css_selector("#onetrust-button-group #onetrust-accept-btn-handler")
        if hasCookieSection:
            cookieSection = self.chrome.find_element_by_css_selector("#onetrust-button-group #onetrust-accept-btn-handler")
            cookieSection.click()

    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()
        try:

            jobsOuter = WebDriverWait(self.chrome, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "js-searchView__jobs"))
            )

            jobContainers = jobsOuter.find_elements_by_css_selector("a[rel = 'noopener']")
            for jobContainer in jobContainers:

                link = jobContainer.get_attribute('href')

                title = jobContainer.find_element_by_css_selector(".m-card-content__inner h3").text
                title = title.strip()
                self.job.setLink(link, trackingVariable=self.jobTrackingVariable)
                self.job.setTitle(title)
                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            jobIndex = 0
            for job in self.jobs:
                self.chrome.getComplete(job.getLink())
                try:
                    WebDriverWait(self.chrome, 100).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div[data-automation-id='jobPostingPage']"))
                    )
                    isJobExists = True
                except Exception as e:
                    exception_message = str(job.getTitle()) + ' : ' + str(e) + "\n"
                    self.exceptionLogging('warning', exception_message)
                    isJobExists = False

                if isJobExists:
                    try:
                        location = self.chrome.find_element_by_css_selector("div[data-automation-id='locations'] dl").text
                        if location is not None:
                            location = location.strip()
                            location = location.replace("locations\n", "")
                            location = location.replace("\n", ", ")
                        self.jobs[jobIndex].setLocation(location)
                    except Exception as e:
                        exception_message = str(job.getTitle()) + ' : ' + str(e) + "\n"
                        self.exceptionLogging('warning', exception_message)

                    # self.chrome.execute_script(
                    #     """
                    #     jQuery("body").find("textarea").remove();
                    #     jQuery("body").find("input").remove();
                    #     jQuery("body").find("button").remove();
                    #     jQuery("body").find("script").remove();
                    #     """
                    # )
                    try:
                        description = self.chrome.find_element_by_css_selector(
                        "div[data-automation-id='jobPostingDescription']").get_attribute("innerHTML")
                        # description = description + self.chrome.find_element_by_css_selector(
                        #     "div[data-metadata-id='richTextArea.siteInfo.aboutUs']").get_attribute("innerHTML")
                        self.jobs[jobIndex].setDescription(description)
                    except Exception as e:
                        exception_message = str(job.getTitle()) + ' : ' + str(e) + "\n"
                        self.exceptionLogging('warning', exception_message)

                    jobIndex = jobIndex + 1
                else:
                    del self.jobs[jobIndex]


            return True

        except:
            self.exceptionLogging()
            return False

