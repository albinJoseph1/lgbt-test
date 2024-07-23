from Companies.Sega.SubAgents.StandardSegaAgent import Agent as ScrapAgent
from Resource import htmlmin

class Agent(ScrapAgent):
    def __init__(self, chrome):
        self.chrome = chrome
        super(Agent, self).__init__(self.chrome)

        #     Company Details Start
        self.companyName = "Relic Entertainment"
        self.companyHint = "Relic Entertainment"
        #     Company Details End