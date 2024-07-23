from abc import ABC, abstractmethod


# Support Modules for Agents
import time
from requests import Session
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

import pathlib
import sys
import os
from Resource import htmlmin
import logging
import datetime
import traceback

from Objects import Job
from Managers import environmentManager
from Managers import errorControlManager

class ScrapAgent(ABC):

    def __init__(self):
        self.feedTypeXML = 'xml'
        self.feedTypeJSON = 'json'
        self.feedTypeWebScrap = 'web-scrap'
        self.jobs = []
        self.job = Job()

        self.companyName = "standardCompanyName"
        self.ownerUsername = "standardUserName"
        self.scrapPageURL = "standardScrapPageUrl"
        self.feedType = self.feedTypeWebScrap
        self.maxScrapPageLimit = 20
        self.agentQueuePriority = 1

    def getCompanyName(self):
        return self.companyName

    def getFeedType(self):
        return self.feedType

    def getFeedUrl(self):
        return self.scrapPageURL

    def getSourceJobCount(self):
        return 0

    def getScrapedJobCount(self):
        return len(self.jobs)

    def getOwnerUsername(self):
        return self.ownerUsername

    @abstractmethod
    def loadJobs(self):
        pass

    @abstractmethod
    def loadScrapPage(self):
        pass

    def addToJobs(self):
        self.jobs.append(self.job)
        self.job = Job()

    def removeElements(self, elementsToBeRemoved: list) -> None :
        """

        :type elementsToBeRemoved: list
        """
        for elementToBeRemoved in elementsToBeRemoved:
            elementIsString = isinstance(elementToBeRemoved,str)
            if elementIsString:
                self.chrome.execute_script("""
                                var FetchedElements = document.querySelectorAll(arguments[0]);
                                for(i=0; i < FetchedElements.length;i++){
                                    FetchedElements[i].remove();
                                }
                            """, elementToBeRemoved)
            else:
                self.chrome.execute_script("""arguments[0].remove()""",elementToBeRemoved)

    def sanitizeElementsForDescription(self, additionalElementsToRemove: list = [], excludeElements: list = []) -> None:
        """

        :type excludeElements: list
        :type additionalElementsToRemove: list
        """
        elementsToBeRemove = ['textarea','input','button','script']
        elementsToBeRemove += additionalElementsToRemove

        for excludeElement in excludeElements:
            elementIndex = 0
            for elementToBeRemove in elementsToBeRemove:
                if elementToBeRemove == excludeElement:
                    del elementsToBeRemove[elementIndex]
                    break
                else:
                    elementIndex = elementIndex + 1

        self.removeElements(elementsToBeRemove)


    def logFileCreation(self,loggingFilePAth,logFileName):
        if not os.path.exists(loggingFilePAth):
            os.makedirs(loggingFilePAth)

        loggingFilePAth = loggingFilePAth + logFileName
        writeloggingFile = open(loggingFilePAth, "a+")

        return writeloggingFile

    def exceptionLogging(self, logType = 'error',exception_message = None):
        loggingFilePAth = environmentManager.formatPath('log/' + self.getCompanyName())
        errorThatFound = traceback.format_exc()
        em = errorControlManager()
        if logType == 'error':

            loggingFilePAth = loggingFilePAth + '/log/error/'

            writeloggingFile = self.logFileCreation(loggingFilePAth,'exception.log')

            writeloggingFile.write(
                "\n***************** Exception logged at" + str(datetime.datetime.now()) + "*****************\n")
            writeloggingFile.write(traceback.format_exc())
            writeloggingFile.write(
                "\n********************************************************************************************\n")

            writeloggingFile.close()

            if 'WebDriverWait' in errorThatFound:
                errorMessage = 'The company site was updated or the company site URL was changed. So, scrapping stoped for this company.'
            elif 'Timed out receiving message from renderer' in errorThatFound:
                errorMessage = 'The company site takes too much time to load. So, scrapping stoped for this company.'
            elif 'title=' in errorThatFound or 'title =' in errorThatFound:
                errorMessage = 'The title of an job in the listing was misssing or an wrong content was present. Please check it.'
            elif 'link=' in errorThatFound or 'link =' in errorThatFound:
                errorMessage = 'The application link of an job in the listing was misssing or the link is on wrong format. It is a must required fild. Please check it.'
            else:
                errorMessage = 'An unknown error was found when trying to Fetch the jobs. Please contact your AWS programming team.'

            em.passErrorToLgbt(errorMessage, self.getCompanyName(), self.getOwnerUsername())


        elif logType == 'warning':
            loggingFilePAth = loggingFilePAth + '/log/warnings/'

            writeloggingFile = self.logFileCreation(loggingFilePAth,'warnings.log')

            writeloggingFile.write(
                "\n***************** Warnings logged at" + str(datetime.datetime.now()) + "*****************\n")
            writeloggingFile.write(exception_message)
            writeloggingFile.close()

        elif logType == 'noJobInfo':
            errorMessage = "There is no adverts found on Listing page. So, We are waiting for any adverts to come to live."
            em.passErrorToLgbt(errorMessage, self.getCompanyName(), self.getOwnerUsername())
