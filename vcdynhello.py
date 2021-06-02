import sys
import argparse
import logging
import json
import datetime

import anticrlf
from veracode_api_py import VeracodeAPI as vapi, Applications, Analyses, DynUtils

DEFAULT_BUSINESS_CRITICALITY = 'HIGH'

log = logging.getLogger(__name__)

def setup_logger():
    handler = logging.FileHandler('vcdynhello.log', encoding='utf8')
    handler.setFormatter(anticrlf.LogFormatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'))
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def creds_expire_days_warning():
    creds = vapi().get_creds()
    exp = datetime.datetime.strptime(creds['expiration_ts'], "%Y-%m-%dT%H:%M:%S.%f%z")
    delta = exp - datetime.datetime.now().astimezone() #we get a datetime with timezone...
    if (delta.days < 7):
        print('These API credentials expire ', creds['expiration_ts'])

def find_app_by_name(search_term):
    return Applications().get_by_name(search_term)

def create_app(name):
    return Applications().create(app_name=name, business_criticality=DEFAULT_BUSINESS_CRITICALITY)

def find_analysis_by_name(name):
    return Analyses().get_by_name(name)

def create_analysis(name,scan,email, owner):
    thescans = [scan]
    return Analyses().create(name=name,scans=thescans, business_unit_guid=None,email=email,owner=owner)

def configure_scan(url, username, password, email, business_owner, phone, app_id):
    theurl = DynUtils().setup_url(url)
    auth_config = DynUtils().setup_auth_config(DynUtils().setup_auth('AUTO',username,password))
    allowed_hosts = [theurl]
    config_request = DynUtils().setup_scan_config_request(url=theurl,allowed_hosts=allowed_hosts,auth_config=auth_config)
    contact = DynUtils().setup_scan_contact_info(email=email,first_and_last_name=business_owner,telephone=phone)
    scan = DynUtils().setup_scan(scan_config_request=config_request,scan_contact_info=contact,linked_app_guid=app_id)
    return scan

def main():
    parser = argparse.ArgumentParser(
        description='This script creates a dynamic analysis from the provided input.')
    parser.add_argument('-u', '--url', required=False, help='URL to scan.',default='https://jarrett2.example.com')
    parser.add_argument('--username', '-n', help='Username to use to authenticate to the URL.',default='admin')
    parser.add_argument('--password', '-p', help='Password to authenticate to the URL (required if --username is set).',default='pwd')
    parser.add_argument('--email','-e', help='Contact email for the scan')
    parser.add_argument('--business_owner','-b', help='Business owner of the system being scanned')
    parser.add_argument('--phone','-ph',help='Contact phone number for the system being scanned')
    args = parser.parse_args()

    url = args.url
    username = args.username
    pwd = args.password
    email = args.email
    bu = args.business_owner
    phone = args.phone
    setup_logger()

    # CHECK FOR CREDENTIALS EXPIRATION
    creds_expire_days_warning()

    # check to see if already an application profile named the URL
    app = find_app_by_name(url)

    if len(app) > 0:
        app_id = app[0]['guid']
        log.info('Found app_id {} for application name {}.'.format(app_id,url))
    else:
        # create the application
        app = create_app(url)
        app_id = app['guid']
        log.info('Created app_id {} for application name {}.'.format(app_id,url))

    # check to see if we already have a dynamic analysis for this URL

    da = find_analysis_by_name(url)

    if len(da) > 0:
        message = 'Found existing analysis named {} (analysis ID {}), exiting'.format(url, da[0]['analysis_id'])
        log.info(message)
        print(message)
        return

    # configure the scan request
    scan = configure_scan(url,username,pwd,email, bu, phone, app_id)

    # create the analysis

    create_analysis(url, scan,email,bu)

    da = find_analysis_by_name(url) # no JSON returned for create_analysis, need to look it up after

    msg = "Created analysis id {} for url {}".format(da[0]['analysis_id'],url)
    print(msg)
    log.info(msg)
    
if __name__ == '__main__':
    main()