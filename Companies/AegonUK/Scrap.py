# Required Packages
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from datetime import datetime
import requests
import os
from bs4 import BeautifulSoup

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Aegon UK"
        self.ownerUsername = "aegon"
        self.authorization = "TkdGbU9EZ3paamt0TlRWaVpDMDBaV00yTFRreVlqZ3RPVFEyTkRZeFpUYzVaR1JoOjd3Y3FzN2d0ZHVma2k4bzI2NGZyZXNjaWY0emV2MHl1eWlmMnU4YjRpYWl1ZjlkbWJzcTZ3NGxodjRwZDE1eHJnYWU2ZGhscXNhb3JlaHhjYnIzejhvM3R4bTE2bm0yMXoweA=="
        self.tokenEndPoint = "https://wd5-services1.myworkday.com/ccx/oauth2/transamerica/token"
        self.scrapePageUrl = "https://wd5-services1.myworkday.com/ccx/service/customreport2/transamerica/AEG_ISU_JobBoard_FindYourFLex/AEG_UK_Job_Requisitions_Job_Board_Find_Your_Flex_RW?format=simplexml"
        self.refreshToken = "7o1chopav3xmlgfdectxl26yp5i9i8g2l0ehvl627y88d1ijffj3vo9teibdvmw6cl1v377ks1s39ghdrrt99ife7s4q0ezwjl6"
        self.feedType = self.feedTypeXML
        self.additionalFetch = True
        #     Company Details End

    def loadScrapPage(self):
        pass

    def loadXML(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic '+self.authorization,
        }
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refreshToken
        }

        response = requests.post(self.tokenEndPoint, headers=headers, data=data)
        json_data = response.json()
        
        headers = {
            'Authorization': 'Bearer '+json_data['access_token'],
            'Cookie': 'TS012df9cf=010758ad2a707d0a6d2f664ea9865812919f1fdf7ec58e8dc7d5a083b702377f671499cb292efb65a78356f1dad0e8a7a382d6d177'
        }

        response = requests.get(self.scrapePageUrl, headers=headers)

        jobDataFilePath = './Companies/Aegon/XMLFeed/'
        jobDataFile = jobDataFilePath + 'jobXMLFeed.xml'
        if not os.path.exists(jobDataFilePath):
            os.makedirs(jobDataFilePath)
        writeJobData = open(jobDataFile, "w+")
        writeJobData.write(response.text)

        root = ET.fromstring(response.text)
        self.jobContainers = root.findall(".//{urn:com.workday.report/AEG_UK_Job_Requisitions_Job_Board_FindYourFlex_RW}Report_Entry")

    # Scraper Function
    def loadJobs(self):
        self.loadXML()
        try:
            for job in self.jobContainers:
                title = job.find('{urn:com.workday.report/AEG_UK_Job_Requisitions_Job_Board_FindYourFlex_RW}title').text
                self.job.setTitle(title)

                apply_link = job.find('{urn:com.workday.report/AEG_UK_Job_Requisitions_Job_Board_FindYourFlex_RW}applicationurl').text
                self.job.setLink(apply_link)

                description = job.find('{urn:com.workday.report/AEG_UK_Job_Requisitions_Job_Board_FindYourFlex_RW}description').text
                self.job.setDescription(description)

                location = job.find('{urn:com.workday.report/AEG_UK_Job_Requisitions_Job_Board_FindYourFlex_RW}displaylocation').text
                self.job.setLocation(location)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            return True

        except:
            self.exceptionLogging()
            return False