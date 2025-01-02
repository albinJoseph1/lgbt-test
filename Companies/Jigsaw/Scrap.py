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
        self.companyName = "Jigsaw"
        self.ownerUsername = "jigsawhomes"
        self.scrapPageURL = "https://careers.jigsawhomes.org.uk/jobs"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        cookieCloseButton = WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".cc-theme-block .cc-dismiss"))
        )
        cookieCloseButton.click()

        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "searchResults"))
        )

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector("#emp-profile_0 > .col-12")
            for jobContainer in jobContainers:

                title = str(jobContainer.find_element_by_css_selector(".jobResultTitle > a").text)
                title = title.strip()
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector(".jobResultTitle > a").get_attribute("href")
                self.job.setLink(link)
                self.chrome.execute_script("""jQuery('.jobDetailsSections .row:nth-child(2)').addClass('scrap_expiry_date')                               
                                            jQuery('.jobDetailsSections .row:nth-child(3)').addClass('scrap_salary')""")


                try:
                    stringDate = jobContainer.find_element_by_css_selector(
                        '.jobDetailsSections .scrap_expiry_date .pb-1').text.strip()

                    try:
                        expireDate = datetime.strptime(stringDate, '%d/%b/%Y').strftime('%Y-%m-%d')
                        self.job.setExpireDate(expireDate)
                    except Exception as e:
                        exception_message = str(title) + ' : ' + str(e) + "\n"
                        self.exceptionLogging('warning', exception_message)
                except Exception as e:
                    exception_message = str(title) + ' : ' + str(e) + "\n"
                    self.exceptionLogging('warning', exception_message)

                self.chrome.execute_script("""jQuery('.jobDetailsSections .currency').remove()                               
                                """)
                salary = jobContainer.find_element_by_css_selector('.jobDetailsSections .scrap_salary .pb-2').text.strip()
                self.job.setSalary(salary)

                location = jobContainer.find_element_by_css_selector('.jobDetailsSections .jobLocation .pb-1').text.strip()
                self.job.setLocation(location)

                expiration_date_row = jobContainer.find_element(By.CSS_SELECTOR, '.fa-calendar').find_element(By.XPATH, '..')
                extractExpireDate = expiration_date_row.text.strip()

                if extractExpireDate is not None:
                    possibleExpiryDateFormats = [
                        "%Y-%m-%d",
                        "%d/%m/%Y",
                        "%d/%b/%Y", 
                    ]
                    for possibleExpireDate in possibleExpiryDateFormats:
                        try:
                            extractExpireDate = datetime.strptime(extractExpireDate, possibleExpireDate).strftime('%Y-%m-%d')
                            self.job.setExpireDate(extractExpireDate)
                        except Exception as e:
                            exception_message = str(title) + ' : ' + str(e) + "\n"
                            self.exceptionLogging('warning', exception_message)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                descriptionElement = self.chrome.find_element_by_xpath('/html/body/div[6]/div[1]/div')
                description = descriptionElement.get_attribute('innerHTML')
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False

