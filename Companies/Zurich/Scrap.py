# Required Packages
from datetime import datetime
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
        self.companyName = "Zurich Insurance"
        self.ownerUsername = "zurichinsurancegroup"
        self.locationKeys = ["GB"]
        self.scrapPageURL = "https://www.careers.zurich.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_shifttype=&optionsFacetsDD_department=&optionsFacetsDD_customfield3="
        self.feedType = self.feedTypeWebScrap
        self.nextPageNo = 2
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        self.chrome.pageWait()
        hasCookieSection = bool(self.chrome.find_element_by_id("cookie-acknowledge"))
        if hasCookieSection:
            cookieSection = self.chrome.find_element_by_id("cookie-close")
            cookieSection.click()
        WebDriverWait(self.chrome, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#searchresults"))
        )

    def nextPage(self):
        self.chrome.pageWait()
        linkText = str(self.nextPageNo)
        hasNextPage = bool(self.chrome.find_elements_by_link_text(linkText))
        self.nextPageNo += 1
        if hasNextPage:
            nextButton = self.chrome.find_element_by_link_text(linkText)
            nextButton.click()
            self.chrome.pageWait()
            return hasNextPage
        else:
            return False

    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()
        try:
            nextStartPage = self.nextPageNo
            for locationKey in self.locationKeys:
                locationFilter = self.chrome.find_element_by_css_selector(".keywordsearch-locationsearch")
                locationFilter.clear()
                locationFilter.send_keys(locationKey)
                self.nextPageNo = nextStartPage
                self.chrome.find_element_by_css_selector(".keywordsearch-button").click()
                self.chrome.pageWait()

                while True:
                    jobContainers = self.chrome.find_elements_by_css_selector("#searchresults tr.data-row")
                    hasMorePlace = bool(self.chrome.find_elements_by_css_selector("span.jobLocation > .nobr"))
                    if hasMorePlace:
                        self.chrome.execute_script("jQuery('span.jobLocation > .nobr').remove()")

                    for jobContainer in jobContainers:

                        location = jobContainer.find_element_by_css_selector("td.colLocation > span.jobLocation").text
                        self.job.setLocation(location)

                        title = str(jobContainer.find_element_by_css_selector("span.jobTitle > a").text)
                        title = title.strip()
                        self.job.setTitle(title)

                        link = jobContainer.find_element_by_css_selector("span.jobTitle > a").get_attribute("href")
                        self.job.setLink(link)

                        self.job.setCompanyName(self.companyName)
                        self.job.setOwnnerUsername(self.ownerUsername)

                        self.addToJobs()

                    if self.nextPage():
                        pass
                    else:
                        break

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())
                self.chrome.pageWait()
                try:
                    descriptionElement = self.chrome.find_element_by_css_selector(".col-xs-12.fontalign-left")
                except:
                    descriptionElement = self.chrome.find_element_by_css_selector(".job")

                self.sanitizeElementsForDescription()

                description = descriptionElement.get_attribute('innerHTML')
                description = htmlmin.minify(description, remove_empty_space=True)
                description = description.replace("\"", "'")
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False

