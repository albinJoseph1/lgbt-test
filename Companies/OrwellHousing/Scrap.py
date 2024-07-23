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
        self.companyName = "Orwell Housing"
        self.ownerUsername = "orwellhousing"
        self.scrapPageURL = "https://careers.orwell-housing.co.uk/index"
        # self.jobTrackingVariable = "source=Aviva_Rec_LGBTjobs"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        cookieSection = WebDriverWait(self.chrome, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#cookieChoiceInfo #cookieChoiceDismiss"))
        )
        cookieSection.click()

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#listing .result"))
        )

    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()
        try:

            jobContainers =self.chrome.find_elements_by_css_selector("#listing .result")
            for jobContainer in jobContainers:

                titleElements = jobContainer.find_elements_by_css_selector(".row .nine .row .six > p")
                for titleElement in titleElements:
                    elements = titleElement.find_element_by_css_selector("span.text__bold").text.strip()
                    if str(elements) == 'Job Title:':
                        title = titleElement.text
                        title = title.replace("Job Title:", "")
                        title = title.strip()
                        break
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector("span[data-format='vacancyLink'] > a").get_attribute('href')
                self.job.setLink(link)

                self.chrome.execute_script(
                    """
                    jQuery(".result .nine .details__container.row .detail__box:first-child").addClass('job_location');
                    
                    """
                )
                location = jobContainer.find_element_by_css_selector(".job_location > p").text
                location = location.strip()
                self.job.setLocation(location)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):

                self.chrome.getComplete(job.getLink())
                self.chrome.pageWait()

                applyLink = self.chrome.find_element_by_css_selector('#vac-apply-top').get_attribute('href')
                applyLink = str(applyLink.replace("rmId=3149", "rmId=3544"))
                applyLink = applyLink.strip()
                self.jobs[currentJobIndex].setLink(applyLink)

                self.sanitizeElementsForDescription()
                descriptionElement = self.chrome.find_element_by_css_selector('#vac-poster')
                description = descriptionElement.get_attribute('innerHTML').strip()
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False

