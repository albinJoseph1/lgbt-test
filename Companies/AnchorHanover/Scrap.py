# Required Packages
from datetime import datetime
from Resource import htmlmin
import time
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
        self.companyName = "Anchor Hanover"
        self.ownerUsername = "anchorhomes"
        self.scrapPageURL = "https://apply.anchorhanover.org.uk/vacancies/?c%5Ball%5D=&submit=Search%23results"
        self.feedType = self.feedTypeWebScrap
        self.maxScrapPageLimit = 20
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        WebDriverWait(self.chrome, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".site-container .vacancy-results .vacancy-results-wrap"))
        )


    def nextPage(self):
        # self.chrome.switch_to_frame(0)
        has_next_page = bool(self.chrome.find_elements_by_css_selector(".paginator .next-page a"))
        if has_next_page:
            next_button = self.chrome.find_element_by_css_selector(".paginator .next-page a")
            next_button.click()
            WebDriverWait(self.chrome, 20).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".site-container .vacancy-results .vacancy-results-wrap"))
            )
            time.sleep(3)
            return has_next_page
        else:
            return False

    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()
        try:
            while True:
                # print("Current page : " + self.chrome.current_url)
                jobContainers = self.chrome.find_elements_by_css_selector(
                    ".site-container .vacancy-results .vacancy-results-wrap")
                for jobContainer in jobContainers:
                    link = jobContainer.find_element_by_css_selector(
                        ".vacancy-results-wrap > a:last-child").get_attribute(
                        'href')
                    self.job.setLink(link)

                    title = jobContainer.find_element_by_css_selector(".vacancy-title").text
                    self.job.setTitle(title)
                    # print("Scraping job : " + title)

                    location = jobContainer.find_element_by_css_selector(".vacancy_result .value_location").text
                    self.job.setLocation(location)

                    hasSalary = bool(jobContainer.find_elements_by_css_selector(".vacancy_result .value_hourly_rate_of_pay"))
                    hourlySalary = None
                    if hasSalary:
                        hourlySalary = jobContainer.find_element_by_css_selector(
                            ".vacancy_result .value_hourly_rate_of_pay").text
                    self.job.setSalaryPerHour(hourlySalary)

                    expireDateText = jobContainer.find_element_by_css_selector(
                        ".vacancy_result .value_closing_date").text
                    try:
                        expireDate = datetime.strptime(expireDateText, '%d/%m/%Y').strftime('%Y-%m-%d')
                        self.job.setExpireDate(expireDate)
                    except Exception as e:
                        exception_message = str(title) + ' : ' + str(e) + "\n"
                        self.exceptionLogging('warning', exception_message)

                    hasContract = bool(jobContainer.find_elements_by_css_selector(".vacancy_result .value_contract"))
                    contract = None
                    if hasContract:
                        contract = str(
                            jobContainer.find_element_by_css_selector(".vacancy_result .value_contract").text)
                        contract = contract.strip()
                    self.job.setContract(contract)

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
                description = self.chrome.find_element_by_css_selector(
                    ".site-container .vacancy_full_description").get_attribute(
                    'innerHTML')
                description = description.replace('\n', '')
                description = description.replace('\u00a3', '&#163;')
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False

