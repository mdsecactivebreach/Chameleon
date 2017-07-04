import sys
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class IBMXforce:

    def __init__(self, domain):
        self.domain = domain
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    # In part ripped from DomainHunter
    # https://github.com/minisllc/domainhunter/blob/master/domainhunter.py
    # Credit: Joe Vest and Andrew Chiles
    def checkIBMxForce(self):
        print('[-] IBM xForce Check: {}'.format(self.domain))
        s = requests.Session()
        useragent = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)'
        try:
            url = 'https://exchange.xforce.ibmcloud.com/url/{}'.format(self.domain)
            headers = {'User-Agent':useragent,
                        'Accept':'application/json, text/plain, */*',
                        'x-ui':'XFE',
                        'Origin':url,
                        'Referer':url}
            url = 'https://api.xforce.ibmcloud.com/url/{}'.format(self.domain)
            response = s.get(url,headers=headers,verify=False)

            responseJson = json.loads(response.text)

            if 'error' in responseJson:
                a = responseJson['error']
            else:
                a = responseJson["result"]['cats']

            print "\033[1;32m[-] Domain categorised as %s\033[0;0m"  % responseJson["result"].get('cats',{}).keys()[0]

        except Exception as e:
            print('[-] Error retrieving IBM x-Force reputation!')
            return "-"

    def submit_category(self):
        print('[-] Submitting {} for Financial category'.format(self.domain))
        s = requests.Session()
        useragent = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)'
        url = 'https://exchange.xforce.ibmcloud.com/url/{}'.format(self.domain)
        headers = {'User-Agent':useragent,
                    'Accept':'application/json, text/plain, */*',
                    'x-ui':'XFE',
                    'Origin':url,
                    'Referer':url,
                    'Content-Type': 'application/json;charset=utf-8'}
        post_data = "{\"feedback\":{\"sourceid\":\"%s\",\"feedbacktext\":\"\",\"current\":{\"urlcategory\":[]},\"proposed\":{\"urlcategory\":[{\"name\":\"Banking\",\"action\":\"ADD\",\"id\":\"53\"}]},\"webApplication\":\"\",\"notify\":true,\"postAsComment\":true}}" % self.domain

        url = 'https://exchange.xforce.ibmcloud.com/api/url/feedback/{}'.format(self.domain)
        response = s.post(url, data = post_data, headers = headers)
        if "Thank you for your time and feedback" in response.content:
            print "[-] Category successfully submitted, please wait an hour"
        else:
            print "[-] Error submitting category"

if __name__ == "__main__":
    url = sys.argv[1]
    xf = IBMXforce(url)
    xf.checkIBMxForce()
    xf.submit_category()
