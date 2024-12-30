import AgentExceptions
import os
import re
from datetime import datetime
from requests import get
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException, NoSuchElementException
from Companies.StandardAgent import ScrapAgent


POSSIBLE_EXPIRYDATE_FORMATS = [
    "%d %B %Y",
    "%A %d %B %Y",
]

class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "East Sussex College"
        self.ownerUsername = "eastsussexcollege"
        self.scrapPageURL = "https://talos360.com/feeds/jobboardonemail5"
        self.passWord = '1z1q&_a6aB8*'
        self.userName = 'lgbtjobsxmlfeed@escg.ac.uk'
        self.feedType = self.feedTypeXML
        #     Company Details End

    def loadScrapPage(self):
        pass

    def loadXML(self):
        responseJobData = get(self.scrapPageURL, auth=(self.userName, self.passWord))
        if responseJobData.status_code == 200:
            self.jobData = BeautifulSoup(responseJobData.text, "xml")

    def parse_and_format_expiration_date(self, title, date_string):
        try:
            # determine_correct_year
            parsedDate = datetime.strptime(date_string, "%A %d %B")
            if parsedDate:
                weekdayDay= date_string.split()[0]
                currentYear = datetime.now().year

                for year in range(currentYear, currentYear + 2):            
                    full_date_string = f"{date_string} {year}"
                    try:
                        parsedDate = datetime.strptime(full_date_string, "%A %d %B %Y")
                        if parsedDate.strftime("%A") == weekdayDay:  # Check if the weekday matches
                            expireDate = parsedDate.strftime("%Y-%m-%d")
                            return expireDate
                    except ValueError:
                        continue

        except ValueError:
            #check other formates
            for possibleExpireDate in POSSIBLE_EXPIRYDATE_FORMATS:
                try:
                    expireDate = datetime.strptime(date_string, possibleExpireDate).strftime('%Y-%m-%d')
                    return expireDate
                except ValueError:
                    continue

        warningMessage = f"Failed to set the expire date for the job: '{title}'. Current expire date is: {date_string}."
        dateWarning=AgentExceptionsishere.ExpiryDateFormatWarning(message = warningMessage)
        dateWarning.gotFormat=date_string
        self.saveWarning(dateWarning)
        return True
    
    def loadJobs(self):
        self.loadXML()
        try:
            jobContainers = self.jobData.find_all('item')
            if not jobContainers:
                errorTitle= "Job Items Element Missing or Not Found"
                raise AgentExceptions.WebDriverWaitError(title=errorTitle)
            
            for index, jobContainer in enumerate(jobContainers):
                title = jobContainer.find('jobtitle')
                if not title:
                    # errorMessage = f"We encountered an issue retrieving the job title for job index {index}."
                    errorTitle= "Title scrapping Error"
                    raise AgentExceptions.NoSuchElementException(message=errorMessage,title=errorTitle)
                title = title.text
                self.job.setTitle(title)

                link = jobContainer.find('link')
                if not link:
                    errorMessage = f"Unable to retrieve Apply link for the job '{title}' from the XML feed."
                    errorTitle= "Apply Link not found"
                    raise AgentExceptions.LinkNotFoundOrFormatError(message=errorMessage, title=errorTitle)
                link = link.text
                self.job.setLink(link)

                description = jobContainer.find('description')
                if not description:
                    errorMessage = f"Unable to retrieve the description for the job '{title}' from the XML feed."
                    errorTitle= "Description scrapping Error"
                    raise AgentExceptions.NoSuchElementException(message=errorMessage, title=errorTitle, pageURL=link)
                description =description.text
                sanitizedDescription= re.sub(r"<p>(?:&nbsp;|\s)*</p>", "", description)
                self.job.setDescription(sanitizedDescription)
                
                PatternForClosingDate = r"Closing\s*date[:\s]*(.*?)(?=\s*<\/p>|\s*<br\s*\/?>|\s*\n)"
                searchPatternResultForClosingDate = re.search(PatternForClosingDate, description, re.IGNORECASE)
                if searchPatternResultForClosingDate:
                    sanitizedClosingDate = re.sub(r"<.*?>|\.", "", searchPatternResultForClosingDate.group(1)).replace("&nbsp;", " ").strip()
                    expireDate = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", sanitizedClosingDate)
                    if re.search( r"\d", expireDate):
                        finalExpireDate = self.parse_and_format_expiration_date(title,expireDate)
                        if finalExpireDate:
                            self.job.setExpireDate(finalExpireDate)

                location = jobContainer.find('joblocation').text
                self.job.setLocation(location)

                salary = "£"+jobContainer.find('jobsalaryfrom').text.split(".")[0] + " to £" + jobContainer.find('jobsalaryto').text.split(".")[0] 
                self.job.setSalary(salary,"£(\d{1,5}(?:,\d{5})*) to £(\d{1,5}(?:,\d{5})*)", is_salary_text=True)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()
            return True
        
        except TimeoutException:
            raise AgentExceptions.TimeOutError()
        
        except WebDriverException:
            raise AgentExceptions.WebDriverWaitError()
        
        except ValueError as e:
            raise AgentExceptions.ValueError(message=str(e))