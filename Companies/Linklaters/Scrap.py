# Required Packages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
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
        self.companyName = "Linklaters"
        self.ownerUsername = "linklaters"
        self.scrapPageURL = "https://linklaters.wd3.myworkdayjobs.com/Linklaters/10/refreshFacet/318c8bb6f553100021d223d9780d30be"
        self.feedType = self.feedTypeWebScrap
        self.jobProfilesToExclude = ['Associate', 'Associate (Knowledge)', 'Man Associate', 'Counsel', 'Lawyer BA', 'Legal Intern']
        self.jobTrackingVariableForLGBT = "source=LGBTJobs"
        self.jobTrackingVariableForBME = "source=BMEJobs"
        self.jobTrackingVariableForDISABILITY = "source=DisabilityJobs"
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        self.acceptCookies()
        self.chrome.maximize_window()
        WebDriverWait(self.chrome, 20).until(
            EC.presence_of_element_located((By.ID, "wd-AdvancedFacetedSearch-facetSearchResult"))
        )

        countryFilters = self.chrome.find_elements_by_css_selector("#wd-Facet-timeType div[data-automation-id='checkbox']")
        countryCheckBoxUK = [country for country in countryFilters if "United Kingdom" == country.text][0]
        countryCheckBoxUK.click()
        
        self.excludeJobProfiles()

        # scroll to page end to load bottom jobs
        self.chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    def acceptCookies(self):
        hasCookie = bool(self.chrome.find_elements_by_css_selector("button[data-automation-id='legalNoticeAcceptButton']"))
        if hasCookie:
            cookieButton = self.chrome.find_element_by_css_selector("button[data-automation-id='legalNoticeAcceptButton']")
            cookieButton.click()
        time.sleep(2)

    def excludeJobProfiles(self):

        wait = WebDriverWait(self.chrome, 60)
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#wd-Facet-workerSubType div[data-automation-id='wd-MoreLink']")))
        time.sleep(2)
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#wd-Facet-workerSubType div[data-automation-id='wd-MoreLink']"))).click()

        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#wd-Facet-workerSubType div[data-automation-id='checkbox']")))
        profileFilters = self.chrome.find_elements_by_css_selector(
            "#wd-Facet-workerSubType div[data-automation-id='checkbox']")
        for profile in profileFilters:
            self.chrome.clickElement(profile)
        time.sleep(2)

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector("#wd-FacetedSearchResult-ResultsPnl-facetSearchResult li[data-automation-id = 'compositeContainer']")
            for jobContainer in jobContainers:
                linkContainer = jobContainer.find_element_by_css_selector("#monikerList div[data-automation-id = 'promptOption']")
                action = ActionChains(self.chrome)
                action.context_click(linkContainer).perform()

                title = jobContainer.find_element_by_css_selector(".gwt-Label[role='link']").text
                self.job.setTitle(title)

                seeInNewWindow_button = self.chrome.find_element_by_css_selector(".wd-popup div[data-automation-id = 'seeInNewWindow']")
                seeInNewWindow_button.click()
                self.chrome.switch_to.window(self.chrome.window_handles[-1])
                wait = WebDriverWait(self.chrome, 60)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-automation-id='job-posting-details']")))

                link = self.chrome.current_url
                link = link + "/apply"
                self.job.setLink(link, self.jobTrackingVariableForLGBT, lgbtManager.site.LGBT)
                self.job.setLink(link, self.jobTrackingVariableForBME, lgbtManager.site.BME)
                self.job.setLink(link, self.jobTrackingVariableForDISABILITY, lgbtManager.site.DISABILITY)

                location = self.chrome.find_element_by_css_selector('div[data-automation-id="locations"]').text
                location = location.replace("locations\n", "")
                self.job.setLocation(location)

                self.sanitizeElementsForDescription()
                description = self.chrome.find_element_by_css_selector('div[data-automation-id="jobPostingDescription"]').get_attribute('innerHTML')
                self.job.setDescription(description)

                self.chrome.close()
                self.chrome.switch_to.window(self.chrome.window_handles[0])
                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            return True

        except:
            self.exceptionLogging()
            return False
