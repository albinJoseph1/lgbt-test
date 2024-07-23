# Required Packages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
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
        self.companyName = "Graham Construction"
        self.ownerUsername = "grahamconstruction"
        self.scrapPageURL = "https://vacancies.graham.co.uk/vacancies/vacancy-search-results.aspx"
        self.feedType = self.feedTypeWebScrap
        self.jobTrackingVariableForLGBT = "source=lgbtjobs"
        self.jobTrackingVariableForBME = "source=bmejobs"
        self.jobTrackingVariableForDISABILITY = "source=disabilityjob"
        self.jobTrackingVariableForNEURODIVERSITY = "source=neurodiversityjobs"
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        self.acceptCookies()
        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, ".vsr-results-grid"))
        )

    def acceptCookies(self):
        hasCookie = bool(self.chrome.find_elements_by_css_selector("#epdsubmit"))
        if hasCookie:
            cookieButton = self.chrome.find_element_by_css_selector("#epdsubmit")
            cookieButton.click()
        time.sleep(2)

    def nextPage(self):
        has_next_page = bool(self.chrome.find_element_by_css_selector('#ctl00_ContentContainer_ctl00_VacancyPager > a:nth-last-of-type(2)').text == 'Next')
        if has_next_page:
            next_button = self.chrome.find_element_by_css_selector('#ctl00_ContentContainer_ctl00_VacancyPager > a:nth-last-of-type(2)')
            next_button.click()
            WebDriverWait(self.chrome, 50).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".vsr-results-grid"))
            )
            return has_next_page
        else:
            return False

    def loadJobs(self):
        self.loadScrapPage()
        try:
            while True:
                jobContainers = self.chrome.find_elements_by_css_selector(".vsr-results-grid .vsr-grid-job")
                for jobContainer in jobContainers:
                    title = jobContainer.find_element_by_css_selector(".vsr-job__title a").text
                    title = title.strip()
                    self.job.setTitle(title)

                    link = jobContainer.find_element_by_css_selector(".vsr-job__title a").get_attribute("href")
                    self.job.setLink(link, self.jobTrackingVariableForLGBT, lgbtManager.site.LGBT)
                    self.job.setLink(link, self.jobTrackingVariableForBME, lgbtManager.site.BME)
                    self.job.setLink(link, self.jobTrackingVariableForDISABILITY, lgbtManager.site.DISABILITY)
                    self.job.setLink(link, self.jobTrackingVariableForNEURODIVERSITY, lgbtManager.site.NEURODIVERSITY)

                    location = jobContainer.find_element_by_css_selector("[data-id='div_content_VacV_AllLocations'] > div span").text
                    self.job.setLocation(location)

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

                title = self.chrome.find_element_by_css_selector("#div_VacV_Description").find_element_by_xpath("preceding-sibling::div[@class='title'][1]").get_attribute('innerHTML')
                description = self.chrome.find_element_by_css_selector("#div_VacV_Description").get_attribute('innerHTML')
                description = title + description

                qualifications = self.chrome.find_element_by_css_selector("#div_VacV_Qualifications").get_attribute('innerHTML')
                if 'Not Specified' not in qualifications:
                    title = self.chrome.find_element_by_css_selector("#div_VacV_Qualifications").find_element_by_xpath("preceding-sibling::div[@class='title'][1]").get_attribute('innerHTML')
                    qualifications = title + qualifications
                    description += qualifications

                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False