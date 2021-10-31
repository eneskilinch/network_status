from selenium import webdriver
from time import sleep
import requests


class UPorDOWN:
    """
    Analyses the all scripts in given partner website

    """

    def __init__(self, website, writeout):
        self.networkList = []
        self.writeout = writeout
        self.driver = webdriver.Chrome()
        self.website = website

    def collect_network(self):
        """
        Collects all files types in network

        """
        self.driver.get(self.website)
        sleep(2)
        self.driver.refresh()
        sleep(2)
        self.networks = self.driver.execute_script(
            "var network = window.performance.getEntries() || {}; return network;")
        return self.select_scripts()

    def select_scripts(self):
        """
        Selects only javascript files in network

        :param writeout: change 27. line to save output of the scripts

        """
        for script in self.networks:
            try:
                if script['initiatorType'] == 'script':
                    self.networkList.append(script['name'])
                    if self.writeout == 'yes':
                        with open('networks.txt', 'a', encoding='utf-8') as network:
                            network.write(script['name'])
                            network.write('\n')
                    else:
                        pass
                else:
                    continue
            except KeyError:
                pass
        self.driver.quit()
        return self.calculation()

    def calculation(self):
        for url in self.networkList:
            response = requests.get(url, allow_redirects=False)
            if response.status_code == 200:
                print(url, '200 OK', response.elapsed.total_seconds())
            else:
                print(url, response.status_code, '\n')
                raise Exception('Response status code is not 200')


start = UPorDOWN('website URL', writeout='no')
start.collect_network()
