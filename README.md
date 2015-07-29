# Monitoring SSL Certificates Expiring date with DataDog

This generates DataDog (http://datadoghq.com) Events and Custom checks with WARNING and ERROR levels, Instead of ploting metrics to a graphic and alerting on that metric.
It also defines how often this test should run to avoid overhead.

Screenshot: http://i62.tinypic.com/33tqqua.png

## How to use
 - Copy the file ssl_check_expire_days.py to the folder /etc/dd-agent/checks.d
 - Copy the file ssl_check_expire_days.yaml to the folder /etc/dd-agent/config.d
 - Edit the file /etc/dd-agent/config.d/ssl_check_expire_days.yaml and include your websites address as well as your thresholds for critical and warning alerts
 - Restart the Datadog Agent 

## How to test the alert
After copying the files and setting the configuration, you can:

### Run it as a regular Python Script
ATTENTION - The script will fail when it looks for the api_key but it can help in case you are modifying the code.

From the folder /opt/datadog-agent/agent, run
```shell
PYTHONPATH=. /opt/datadog-agent/embedded/bin/python /etc/dd-agent/checks.d/ssl_check_expire_days.py
```
### Run as a DataDog Test
It will show you some information about the Event contents and so on: 
```shell 
sudo -u dd-agent dd-agent check ssl_check_expire_days
```

## Credits
Based on https://github.com/dobber/datadog-ssl-check-expire-days:

"This is a cool way to check the expire date for all your SSL sites. Now instead of adding calendar events, you can just do monitoring with alerting

The original source is https://workshop.avatarnewyork.com/project/datadog-ssl-expires-check/ and I just changed the way it works.
On the original source, it checked for certificates in the file system. On my version, the script checks for web site certificates.

For information on how to set it up, go to the original author's web site. Only difference is in the yaml file.

All credits to the original author.

I love datadog :) "
