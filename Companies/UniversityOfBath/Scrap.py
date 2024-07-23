# Required Packages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage=None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "University of Bath"
        self.ownerUsername = "universityofbath"
        self.scrapPageURL = "https://www.bath.ac.uk/jobs/vacancies.aspx?cat=-1"
        self.feedType = self.feedTypeWebScrap
        self.defaultLocation = "Bath"
        #     Company Details End

    def loadScrapPage(self):

        self.chrome.getComplete(self.scrapPageURL)

        cookieSection = WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_frameworkHeader_ctl03_ctl02_btnLink"))
        )
        cookieSection.click()

        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#maincontent .vacancyCategoryContainer .vacancyCategoryItem"))
        )

    # Scraper Function
    def loadJobs(self):

        self.loadScrapPage()

        try:

            jobContainers = self.chrome.find_elements_by_css_selector(".vacancyCategoryContainer .vacancyCategoryItem")
            for jobContainer in jobContainers:

                title = str(jobContainer.find_element_by_css_selector(".vacancyCategoryItemTitle > a").text)
                title = title.strip()
                self.job.setTitle(title)

                location = self.defaultLocation
                self.job.setLocation(location)

                link = jobContainer.find_element_by_css_selector(".vacancyCategoryItemTitle > a").get_attribute("href")
                self.job.setLink(link)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)
                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())
                self.chrome.pageWait()
                
                try:
                    fieldContainer = self.chrome.find_elements_by_css_selector('#mainwidgets .mainwidgetcontent p')
                    closingDate = 'None'
                    interviewDate = 'None'
                    for sEelment in fieldContainer:
                        hasWidget = bool(sEelment.find_elements_by_css_selector('.vacancyAdvertWidgetTitle'))
                        if hasWidget:
                            widgetTitle = sEelment.find_element_by_css_selector('.vacancyAdvertWidgetTitle')

                            if str(widgetTitle.text) == 'Salary':
                                salary = sEelment.text
                                salary = salary.strip()
                                salary = salary.replace("Salary", "")
                                salary = salary.replace("\n", "")
                                self.jobs[currentJobIndex].setSalary(salary)

                            if (str(widgetTitle.text) == 'Interview date') and ('To be confirmed' not in sEelment.text) and ('See advert' not in sEelment.text) and ('Open Until Filled' not in sEelment.text) : 
                                interviewDate = sEelment.text
                                interviewDate = interviewDate.strip()
                                interviewDate = interviewDate.replace("Interview date", "")
                                interviewDate = interviewDate.replace("\n", "")
                                
                            elif str(widgetTitle.text) == 'Closing date':
                                closingDate = sEelment.text
                                closingDate = closingDate.strip()
                                closingDate = closingDate.replace("Closing date", "")
                                closingDate = closingDate.replace("\n", "")

                except Exception as e:
                    exception_message = str(job.getTitle()) + ' : ' + str(e) + "\n"
                    self.exceptionLogging('warning', exception_message)

                if interviewDate != 'None':
                    expireDate = interviewDate
                else:
                    expireDate = closingDate
                
                possibleExpiryDateFormats = [
                                "%A %d %B %Y"
                            ]
                for possibleExpireDate in possibleExpiryDateFormats:
                    try:
                        expireDate = datetime.strptime(expireDate, possibleExpireDate).strftime('%Y-%m-%d')
                        self.jobs[currentJobIndex].setExpireDate(expireDate)
                    except Exception as e:
                        exception_message = str(title) + ' : ' + str(e) + "\n"
                        self.exceptionLogging('warning', exception_message)

                self.sanitizeElementsForDescription()
                descriptionElement = self.chrome.find_element_by_css_selector('#maincontent')
                self.chrome.execute_script("""jQuery('#maincontent #vacancyAdvertWidget, #maincontent a[name=top]').remove()
                var locateElm = jQuery('#maincontent .emailDetailsLink').parent('p')
                locateElm.nextAll().remove() 
                locateElm.remove()
                """)
                description = descriptionElement.get_attribute('innerHTML').strip()
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False
