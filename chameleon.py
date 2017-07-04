import argparse
import sys
from modules import *

class Chameleon:

    def __init__(self):
        pass

    def validate_args(self):
        parser = argparse.ArgumentParser(description = "")
        parser.add_argument("--proxy", metavar="<proxy>", dest = "proxy", default = None, help = "Proxy type: a = all, b = bluecoat, m = mcafee, i = IBM Xforce")
        parser.add_argument("--check", action='store_true', help = "Perform check on current category")
        parser.add_argument("--submit", action='store_true', help = "Submit new category")
        parser.add_argument("--domain", metavar="<domain>", dest = "domain", default = None, help = "Domain to validate")
        args = parser.parse_args()

        if not args.proxy:
            print "[-] Missing --proxy argument"
            sys.exit(-1)
        if not args.domain:
            print "[-] Missing --domain argument"
            sys.exit(-1)
        if not args.check and not args.submit:
            print "[-] Missing --check or --submit argument"
            sys.exit(-1)
        return args

    def show_banner(self):
        with open('banner.txt', 'r') as f:
            data = f.read()
            print "\033[92m%s\033[0;0m" % data

    def run(self, args):
        if args.proxy == 'm':
            print "\033[1;34m[-] Targeting McAfee Trustedsource\033[0;0m"
            ts = trustedsource.TrustedSource(args.domain)
            if args.check:
                ts.check_category(False)
            elif args.submit:
                ts.check_category(True)

        if args.proxy == 'b':
            print "\033[1;34m[-] Targeting Bluecoat WebPulse\033[0;0m"
            if args.check:
                b = bluecoat.Bluecoat(args.domain, 'https://www.bloomberg.com')
                b.check_category()
            elif args.submit:
                print "\033[1;31m[-] WARNING: This module must be run from the webserver you want to categorise\033[0;0m"
                print "\033[1;31m[-] Proceed: Y/N\033[0;0m"
                while True:
                    choice = raw_input().lower()
                    if choice == 'Y' or choice =='y':
                        b = bluecoat.Bluecoat(args.domain, 'https://www.bloomberg.com')
                        b.run()
                        return True
                    elif choice == 'N' or choice == 'n':
                        return False

        if args.proxy == 'i':
            print "\033[1;34m[-] Targeting IBM Xforce\033[0;0m"
            xf = ibmxforce.IBMXforce(args.domain)
            if args.check:
                xf.checkIBMxForce()
            elif args.submit:
                xf.submit_category()

        if args.proxy == 'a':
            if args.check:
                print "\033[1;34m[-] Targeting Bluecoat WebPulse\033[0;0m"
                b = bluecoat.Bluecoat(args.domain, 'https://www.bloomberg.com')
                b.check_category()
                print "\033[1;34m[-] Targeting McAfee Trustedsource\033[0;0m"
                ts = trustedsource.TrustedSource(args.domain)
                ts.check_category(False)
                print "\033[1;34m[-] Targeting IBM Xforce\033[0;0m"
                xf = ibmxforce.IBMXforce(args.domain)
                xf.checkIBMxForce()
            elif args.submit:
                print "\033[1;34m[-] Targeting Bluecoat WebPulse\033[0;0m"
                print "\033[1;31m[-] WARNING: This module must be run from the webserver you want to categorise\033[0;0m"
                print "\033[1;31m[-] Proceed: Y/N\033[0;0m"
                while True:
                    choice = raw_input().lower()
                    if choice == 'Y' or choice =='y':
                        b = bluecoat.Bluecoat(args.domain, 'https://www.bloomberg.com')
                        b.run()
                        break
                    elif choice == 'N' or choice == 'n':
                        return False
                print "\033[1;34m[-] Targeting McAfee Trustedsource\033[0;0m"
                ts = trustedsource.TrustedSource(args.domain)
                ts.check_category(True)
                print "\033[1;34m[-] Targeting IBM Xforce\033[0;0m"
                xf = ibmxforce.IBMXforce(args.domain)
                xf.checkIBMxForce()
                xf.submit_category()

if __name__ == "__main__":
    c = Chameleon()
    c.show_banner()
    args = c.validate_args()
    c.run(args)
