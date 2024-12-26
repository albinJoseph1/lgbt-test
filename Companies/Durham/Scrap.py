# Required Packages
import AgentExceptions
from datetime import datetime
from datetime import timedelta
from Resource import htmlmin
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException, NoSuchElementException

from Companies.StandardAgent import ScrapAgent
import re
POSSIBLE_EXPIRYDATE_FORMATS = [
    '%d-%b-%Y, %H:%M:%S AM',
    '%d-%b-%Y, %H:%M:%S PM'
]

class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Durham University"
        self.ownerUsername = "durham"
        self.location = "Durham"
        self.scrapPageURL = "https://durham.taleo.net/careersection/du_ext/jobsearch.ftl"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.ID, "jobsTableContainer"))
        )

    def nextPage(self):

        has_next_button = bool(self.chrome.find_elements(By.CSS_SELECTOR, "#jobPager > .pagersectionpanel:last-child a"))

        if has_next_button:
            next_button = self.chrome.find_element(By.CSS_SELECTOR,'#jobPager > .pagersectionpanel:last-child a')
            has_next_page = next_button.get_attribute("class") != "navigation-link-disabled"
            if has_next_page:
                next_button.click()
                time.sleep(3)
                return has_next_page
            else:
                return False

    def loadJobs(self):
        try:
            self.loadScrapPage()
            havejobContainers = bool(self.chrome.find_elements(By.CSS_SELECTOR, "#jobs .jobsbody tr"))
            if not havejobContainers:
                errorTitle= "Job Items Missing or Element Not Found"
                raise AgentExceptions.WebDriverWaitError(title=errorTitle)
            while True:
                jobContainers = self.chrome.find_elements(By.CSS_SELECTOR, "#jobs .jobsbody tr")
                for index, jobContainer in enumerate(jobContainers):
                    try:
                        title = str(jobContainer.find_element(By.CSS_SELECTOR,"th[scope = 'row'] a").text)
                        title = title.strip()
                        self.job.setTitle(title)
                    except NoSuchElementException as e:
                        errorMessage = f"We encountered an issue while retrieving the job title for job index {index}."
                        errorTitle= "Title scrapping Error"
                        raise AgentExceptions.NoSuchElementException(message=errorMessage,title=errorTitle, actualException=e)

                    try:
                        link = jobContainer.find_element(By.CSS_SELECTOR,"th[scope = 'row'] a").get_attribute("href")
                        self.job.setLink(link)
                    except NoSuchElementException as e:
                        errorMessage = f"Unable to retrieve Apply link for the job '{title}' from the listing page."
                        errorTitle= "Apply Link not found"
                        raise AgentExceptions.LinkNotFoundOrFormatError(message=errorMessage, title=errorTitle, actualException=e)

                    salary = jobContainer.find_element(By.CSS_SELECTOR,"td:nth-of-type(2)").text
                    self.job.setSalaryText(salary)
                    formatted_salary = re.sub(r'\s*to\s*', ' - ', salary)
                    formatted_salary = re.sub(r'[^\d\s\-]', '', formatted_salary).strip()
                    formatted_salary = re.sub(r'\s*-\s*', ' - ', formatted_salary)
                    if re.match(r'^\d+(?:\s*-\s*\d+)?$', formatted_salary):
                        self.job.setSalary(formatted_salary)

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

                hasExpireDate = bool(self.chrome.find_elements(By.ID, "requisitionDescriptionInterface.reqUnpostingDate.row1"))
                checkExpireDate = self.chrome.find_element(By.ID, "requisitionDescriptionInterface.reqUnpostingDate.row1").text
                checkExpireDate = checkExpireDate[0].isdigit()

                if hasExpireDate and checkExpireDate:
                    expireDate = self.chrome.find_element(By.ID, "requisitionDescriptionInterface.reqUnpostingDate.row1").text
                    for possibleExpireDate in POSSIBLE_EXPIRYDATE_FORMATS:
                        try:
                            expireDate = datetime.strptime(expireDate, possibleExpireDate)
                            expireDate = expireDate + timedelta(days=1)
                            expireDate = expireDate.strftime('%Y-%m-%d')
                            self.jobs[currentJobIndex].setExpireDate(expireDate)
                            break
                        except ValueError:
                            continue
                    else:
                        warningMessage = f"Failed to set the expire date for job {job.getTitle()}."
                        dateWarning=AgentExceptions.ExpiryDateFormatWarning(message=warningMessage,pageURL=job.getLink())
                        dateWarning.gotFormat = expireDate
                        self.saveWarning(dateWarning)

                self.sanitizeElementsForDescription()
                try:
                    descriptionOuter = self.chrome.find_element(By.ID, "requisitionDescriptionInterface.descRequisition")
                    description = descriptionOuter.find_element(By.CSS_SELECTOR,".editablesection > .contentlinepanel:nth-last-child(2)").get_attribute("innerHTML") + descriptionOuter.find_element(By.CSS_SELECTOR,".editablesection > .contentlinepanel:nth-last-child(1)").get_attribute("innerHTML")

                    emptyTagPattern = r'<o:p>\s*&nbsp;\s*<\/o:p>'
                    description = re.sub(emptyTagPattern, '', description)
                    stylesRemovedDescription = re.sub(r'style="[^"]*"', '', description)
                    listPattern = r'&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(.*?)(?=&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|</)'
                    listAddedDescription = re.sub(listPattern, r'<ul><li>\1</li></ul>', stylesRemovedDescription)
                    removeUnwantedNBSPPattern = r'(&nbsp;\s*)\1+'
                    description = re.sub(removeUnwantedNBSPPattern, r'&nbsp;', listAddedDescription)
                    unwantedSpaceRemovePattern = r'<\w+[^>]*>&nbsp;<\/\w+>'
                    finalDescription = re.sub(unwantedSpaceRemovePattern, '', description)
                    self.jobs[currentJobIndex].setDescription(finalDescription)

                except NoSuchElementException as e:
                    errorMessage = f"Unable to retrieve the description for the job '{job.getTitle()}' from its single-page."
                    errorTitle= "Description scrapping Error"
                    actualExceptionMessage = f"The 'job description' for the job '{job.getTitle()}' Could not be retrieved from its single-page API.\nHere is the page link : {job.getLink()}"
                    raise AgentExceptions.NoSuchElementException(message=errorMessage, title=errorTitle, actualException=actualExceptionMessage, pageURL=job.getLink())

            return True

        except TimeoutException:
            raise AgentExceptions.TimeOutError()
        
        except WebDriverException:
            raise AgentExceptions.WebDriverWaitError()
        
        except ValueError as e:
            raise AgentExceptions.ValueError(message=str(e))
