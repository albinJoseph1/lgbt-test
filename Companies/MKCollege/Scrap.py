# Required Packages
import AgentExceptions
from selenium.webdriver.common.by import By
from datetime import datetime
from Resource import htmlmin
from datetime import datetime
import re
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from Companies.StandardAgent import ScrapAgent

POSSIBLE_EXPIRYDATE_FORMATS = [
    "%H:%M, %a, %d %b %Y",
    "%H:%M, %a, %d %m %Y",
    "%Y-%m-%d",
    "%d/%m/%Y"
]

class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0
        #     Company Details Start
        self.companyName = "Milton Keynes College"
        self.ownerUsername = "sallyrollings"
        self.scrapPageURL = ['https://www.mkcollege.ac.uk/prison-services/vacancies/', 'https://www.mkcollege.ac.uk/working-for-us/vacancies/']
        self.feedType = self.feedTypeWebScrap
        self.jobKey = 'title'
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

    # Scraper Function
    def loadJobs(self):
        jobLinks = []
        jobsCount = 0
        jobTitles = []

        try:
            for scrapPageURL in self.scrapPageURL:
                self.chrome.getComplete(scrapPageURL)
                jobElements = self.chrome.find_elements(By.CSS_SELECTOR, ".vacancy")
                if not jobElements:
                    errorTitle= "No jobs were found, or the page structure updated"
                    raise AgentExceptions.WebDriverWaitError(title=errorTitle)
                
                for index, jobElement in enumerate(jobElements):
                    try:
                        jobTitle = jobElement.find_element(By.CSS_SELECTOR, ".vacancy-title").text
                    except NoSuchElementException as e:
                        errorMessage = f"We encountered an issue while retrieving the job title for job index {index}."
                        errorTitle= "Title scrapping Error"
                        raise AgentExceptions.NoSuchElementException(message=errorMessage,title=errorTitle, actualException=e)
                    if jobTitle in jobTitles:
                        warningMessage=f"Skipped Job:'{jobTitle}', due to Job with same title already scraped"
                        skippedJobsWarning=AgentExceptions.SkippedJobsWarning(message=warningMessage)
                        skippedJobsWarning.reason = "Duplicate Title"
                        self.saveWarning(skippedJobsWarning)
                        continue
                    # Exclude jobs having 'INTERNAL APPLICATIONS ONLY' in the title
                    if 'INTERNAL APPLICANTS ONLY' in jobTitle.upper() or 'INTERNAL ONLY' in jobTitle.upper():
                        jobsCount -= 1
                        warningMessage=f"Skipped Job:'{jobTitle}', due to 'INTERNAL APPLICANTS ONLY' contained in the tilte"
                        skippedJobsWarning=AgentExceptions.SkippedJobsWarning(message=warningMessage)
                        skippedJobsWarning.reason = "Under in the Rule of Excluding the job Title"
                        self.saveWarning(skippedJobsWarning)
                        continue
                    
                    jobTitles.append(jobTitle)
                    try:
                        jobLinkElement = jobElement.find_element(By.CSS_SELECTOR, ".vacancy-content a")
                        jobLinks.append(jobLinkElement.get_attribute("href"))
                        jobsCount += len(jobLinks)
                    except NoSuchElementException as e:
                        errorMessage = f"Unable to retrieve Apply link for the job '{jobTitle}' from the listing page."
                        errorTitle= "Apply Link not found"
                        raise AgentExceptions.LinkNotFoundOrFormatError(message=errorMessage, title=errorTitle, actualException=e)

            for index, jobLink in enumerate(jobLinks):
                self.chrome.getComplete(jobLink)
                try:
                    title = self.chrome.find_element(By.CSS_SELECTOR, "table.form tbody tr td > h1").text
                    self.job.setTitle(title)
                except NoSuchElementException as e:
                    errorMessage = f"We encountered an issue while retrieving the job title for job index {index}."
                    errorTitle= "Title scrapping Error"
                    raise AgentExceptions.NoSuchElementException(message=errorMessage,title=errorTitle, actualException=e)
                
                link = jobLink
                self.job.setLink(link)

                expireDate = self.chrome.execute_script('''
                        expireDateString = jQuery("#dlAdvertDetails table.form tbody tr:eq(2) td:eq(1)").text();
                        return expireDateString
                ''')
                expireDate = expireDate.strip()
                expireDate = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', expireDate)

                for possibleExpireDate in POSSIBLE_EXPIRYDATE_FORMATS:
                    try:
                        extractExpireDate = datetime.strptime(expireDate, possibleExpireDate).strftime('%Y-%m-%d')
                        self.job.setExpireDate(extractExpireDate)
                        break
                    except ValueError:
                        continue
                else:
                    warningMessage = f"An issue occurred while scraping the job: {title}. Failed to set the expire date (expected format: %Y-%m-%d). The job's current expire date is: {expireDate}."
                    dateWarning=AgentExceptions.ExpiryDateFormatWarning(message = warningMessage)
                    dateWarning.gotFormat=expireDate
                    self.saveWarning(dateWarning)


                location = self.chrome.execute_script('''
                        expireDateString = jQuery("#dlAdvertDetails table.form tbody tr:eq(3) td:eq(1)").text();
                        return expireDateString
                ''')
                location = location.strip()
                self.job.setLocation(location)

                try:
                    self.sanitizeElementsForDescription()

                    descriptionElement = self.chrome.find_element(By.CSS_SELECTOR, "table.form tbody tr.description td")
                    description = descriptionElement.get_attribute('innerHTML')
                    styleRemovedDescription = re.sub(r'style="[^"]*"', '', description).strip()
                    self.job.setDescription(styleRemovedDescription)
                except NoSuchElementException as e:
                    errorMessage = f"Unable to retrieve the description for the job '{title}' from its single-page."
                    errorTitle= "Description scrapping Error"
                    actualExceptionMessage = f"The 'job description' for the job '{title}' Could not be retrieved from its single-page API.\nHere is the page link : {link}"
                    raise AgentExceptions.NoSuchElementException(message=errorMessage, title=errorTitle, actualException=actualExceptionMessage, pageURL=link)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            return True
        
        except NoSuchElementException:
            raise AgentExceptions.NoSuchElementException()

        except TimeoutException:
            raise AgentExceptions.TimeOutError()
        
        except WebDriverException:
            raise AgentExceptions.WebDriverWaitError()

        except ValueError as e:
            raise AgentExceptions.ValueError(message=str(e))
