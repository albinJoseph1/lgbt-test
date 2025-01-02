# Required Packages
import requests
import json
import re
import AgentExceptions
from html import unescape
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Companies.StandardAgent import ScrapAgent
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException

DATE_PATTERN = r"End Date: ([A-Za-z]+ \d{1,2}, \d{4})"
POSSIBLE_EXPIRYDATE_FORMATS = ['%Y-%m-%d']
SALARY_CLEANING_PATTERN = r'</?(b|span)\b[^>]*>'
SALARY_PATTERN = r'£\s*\d+(?:,\d+)*(?:\s*-\s*£\s*\d+(?:,\d+)*)?'
SALARY_WITH_CONTEXT_PATTERN = r'£\s*\d+(?:,\d+)*(?:\s*-\s*£\s*\d+(?:,\d+)*)?.*?(?=<\/\w+>|<br\s*\/?>|<p\s*[^>]*?>)'

class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0
        #     Company Details Start
        self.companyName = "Witherslack Group Ltd"
        self.ownerUsername = "witherslackgroup"
        self.scrapPageURL = "https://witherslackgroup.wd3.myworkdayjobs.com/wday/cxs/witherslackgroup/Witherslack/jobs"
        self.feedType = self.feedTypeJSON
        self.singlePageApiEndpointURL = "https://witherslackgroup.wd3.myworkdayjobs.com/wday/cxs/witherslackgroup/Witherslack"
        self.headers = {
            'content-type': 'application/json'
        }
        #     Company Details End

    def loadScrapPage(self):
        pass

    def fetchAllJobs(self):
        jobs = []
        params = {
            'offset': 0,
            'limit': 20 
        }
        response = requests.post(self.scrapPageURL, headers=self.headers, json=params)
        data = response.json()
        jobs.extend(data['jobPostings'])
        total_jobs = data['total']
        
        while len(jobs) < total_jobs:
            params['offset'] += params['limit']
            response = requests.post(self.scrapPageURL, headers=self.headers, json=params)
            data = response.json()
            jobs.extend(data['jobPostings'])    
        return jobs

    # Scraper Function
    def loadJobs(self):
        try:
            all_jobs = self.fetchAllJobs()
            for index, job in enumerate(all_jobs):
                title = job.get('title')
                if title is None:
                    errorMessage = f"We encountered an issue while retrieving the 'Job Title' at index value '{index}'."
                    errorTitle= "Title fetching Error"
                    actualExceptionMessage = f"Unable to retrieve the 'Job Title' at index {index}. The field('title') is either missing or does not match the expected format."
                    raise AgentExceptions.TitleNotFoundOrFormatError(message=errorMessage,title=errorTitle,actualException=actualExceptionMessage)
                self.job.setTitle(title)

                if job.get('externalPath') is None:
                    errorMessage = f"Unable to retrieve 'external link' for the job '{title}' from job's API."
                    errorTitle= "External Path fetching Error"
                    actualExceptionMessage = f"The filed 'externalPath' for the job '{title}' is either missing or cannot be accessed, preventing us from retrieving the job details."
                    raise AgentExceptions.LinkNotFoundOrFormatError(message=errorMessage, title=errorTitle, actualException=actualExceptionMessage)
                
                singlePageAPIEndpoint = self.singlePageApiEndpointURL + job.get('externalPath')
                self.job.setLink(singlePageAPIEndpoint)
                location = job.get('locationsText')
                self.job.setLocation(location)
                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)
                self.addToJobs()
            
            jobIndex = 0
            for job in self.jobs:
                singlePageAPIEndpoint = job.getLink()
                response = requests.get(singlePageAPIEndpoint)
                job_data = response.text
                json_content = json.loads(job_data)

                applyLink = json_content.get('jobPostingInfo', {}).get('externalUrl')
                if not applyLink:
                    errorMessage = f"Unable to retrieved the apply link for job '{job.getTitle()}' from the job's single-page API."
                    errorTitle= "Apply Link scrapping Error"
                    actualExceptionMessage = f"The 'apply link' for the job '{job.getTitle()}' Could not be retrieved from its single-page API.\nHere is the single page api link '{singlePageAPIEndpoint}'"
                    raise AgentExceptions.LinkNotFoundOrFormatError(message=errorMessage, title=errorTitle, actualException=actualExceptionMessage, pageURL=singlePageAPIEndpoint)
                self.jobs[jobIndex].setLink(applyLink)

                if bool(json_content['jobPostingInfo']['timeType']):
                    contractType = json_content['jobPostingInfo']['timeType']
                    self.jobs[jobIndex].setContract(contractType)
                
                jobDescription = json_content.get('jobPostingInfo', {}).get('jobDescription')
                if not jobDescription:
                    errorMessage = f"Unable to retrieve the description for the job '{job.getTitle()}' from its single-page API."
                    errorTitle= "Description scrapping Error"
                    actualExceptionMessage = f"The 'job description' for the job '{job.getTitle()}' Could not be retrieved from its single-page API.\n Here is the API endpoint: '{singlePageAPIEndpoint}' \n.Here is the page link : {applyLink}"
                    raise AgentExceptions.NoSuchElementException(message=errorMessage, title=errorTitle, actualException=actualExceptionMessage, pageURL=singlePageAPIEndpoint)

                removeBRTags = re.sub(r'<br\s*/?>', '', jobDescription)
                listItemFormateForPTags = re.sub(r'<li>\s*<p>(.*?)</p>\s*</li>', r'<li>\1</li>', removeBRTags)
                listItemFormateForH2BoldTags = re.sub(r'<h2><b>(.*?)</b></h2>', r'<h4><b>\1</b></h4>', listItemFormateForPTags)
                listItemFormateForH2Tags = re.sub(r'<li><h2>(.*?)</h2></li>', r'<li>\1</li>', listItemFormateForH2BoldTags)
                replaceAllH2Tags = re.sub(r'<h2>(.*?)</h2>', r'<p>\1</p>', listItemFormateForH2Tags)
                emptyTagPattern = r'<(p|span|div|li|b|i|strong|em)[^>]*>(\s*|&nbsp;|<span><span>&nbsp;</span></span>)</\1>'
                emptyTagsRemoved = re.sub(emptyTagPattern, '', replaceAllH2Tags)
                listItemFormateForH4Tags = re.sub(r'<li><h4>(.*?)</h4></li>', r'<li>\1</li>', emptyTagsRemoved)

                self.jobs[jobIndex].setDescription(listItemFormateForH4Tags)
                cleanedDescriptionForSalary = re.sub(SALARY_CLEANING_PATTERN, '', jobDescription)
                salarySentenceExtracted = re.search(SALARY_WITH_CONTEXT_PATTERN, cleanedDescriptionForSalary)
                if salarySentenceExtracted:
                    salaryText = unescape(salarySentenceExtracted.group(0))
                    self.jobs[jobIndex].setSalaryText(salaryText)
                    salary = re.findall(SALARY_PATTERN, salaryText)
                    salaryValue = salary[0]
                    salary = re.sub(r'[£,]', '', salaryValue).strip()
                    self.jobs[jobIndex].setSalary(salary)

                if bool(json_content['jobPostingInfo']['endDate']):
                    expireDate = json_content['jobPostingInfo']['endDate']  
                    for possibleExpireDate in POSSIBLE_EXPIRYDATE_FORMATS:
                        try:
                            extractExpireDate = datetime.strptime(expireDate, possibleExpireDate).strftime('%Y-%m-%d')
                            self.jobs[jobIndex].setExpireDate(extractExpireDate)
                            break
                        except ValueError:
                            continue
                    else:
                        warningMessage = f"Failed to set the expire date for job {job.getTitle()}."
                        dateWarning=AgentExceptions.ExpiryDateFormatWarning(message=warningMessage,pageURL=job.getLink())
                        dateWarning.gotFormat = extractExpireDate
                        self.saveWarning(dateWarning)

                jobIndex = jobIndex + 1
            return True

        except TimeoutException:
            raise AgentExceptions.TimeOutError()
        
        except WebDriverException:
            raise AgentExceptions.WebDriverWaitError()