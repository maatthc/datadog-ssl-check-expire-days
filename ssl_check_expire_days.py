# A rewrite of https://workshop.avatarnewyork.com/project/datadog-ssl-expires-check/
# I prefer to test the site itself instead of the ssl cert file

import time
import datetime
import subprocess
import sys
from hashlib import md5

from checks import AgentCheck

# Default Alert Text
Alert_name = "SSL Certificate is about the expire"
# Use this to instruct your team on how to renew the Certificate
Check_Message = "Please consult here (xx) to see how to renew it. "

 
class SSLCheckExpireDays(AgentCheck):
    def check(self, instance):
        Critical = int(instance.get('thresholds').get('critical'))
        Warning = int(instance.get('thresholds').get('warning'))

        site = instance['site']
        p = subprocess.Popen("echo | openssl s_client -connect " + site + ":443 2>/dev/null | openssl x509 -noout -dates | grep notAfter | cut -f 2 -d\= | xargs -0 -I arg date -d arg \"+%s\"",stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if output:
            output = output.rstrip("\n")
            d0 = int(time.time())
            d1 = int(output)
            delta = d1 - d0
            days_to_expire= delta/24/60/60 # convert the timestamp to days
            tag="site:" + site # generate the tags
            print "\nDays to expire: %s - To be Critical should be less than:  %s - To be Warnings should be less than: %s ." % (days_to_expire,Critical,Warning)
            print "tag: " + str(tag)
            #self.gauge(metric, int(days), tags=[tag])
            if days_to_expire < Critical:
                self.event_expire("error", instance, days_to_expire)
                self.service_check(Alert_name,2,None,None,None,None,Check_Message)
            elif days_to_expire < Warning:
                self.service_check(Alert_name,1,None,None,None,None,Check_Message)
                self.event_expire("warning", instance, days_to_expire)
            else:
                # All good
                self.service_check(Alert_name,0,None,None,None,None,Check_Message)

        else:
            #self.gauge(metric, -1, tags=[site])
            self.service_check("Failed to check SSL Certificate for the site %s" %site,1)

    def event_expire (self, level, instance, days_to_expire):
         #self.log.info("%s %s - %s" %(Alert_name,days_to_expire,level))
         # Use a hash of the URL as an aggregation key
         aggregation_key = md5(instance['site']).hexdigest()
         self.event({
            'timestamp': int(time.time()),
            'event_type': 'SSLCertificateExpire',
            'msg_title': Alert_name,
            'msg_text': '%s : %s .It is %s days to expire!' %(Alert_name,instance['site'],days_to_expire),
            'aggregation_key': aggregation_key,
            'alert_type': level
        })

# There is only here to make it easy to test/dev the Check outside the DataDog Agent Environment, e.g. from a IDE
if __name__ == '__main__':
    check, instances = SSLCheckExpireDays.from_yaml('/etc/dd-agent/conf.d/ssl_check_expire_days.yaml')
    for instance in instances:
        print "\nRunning the check against cert: %s ." % (instance['site'])
        check.check(instance)
        if check.has_events():
            print 'Events: %s' % (check.get_events())
        print 'Metrics: %s' % (check.get_metrics())

