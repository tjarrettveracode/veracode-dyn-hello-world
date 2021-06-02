# Veracode Dynamic Hello World

Simple script that demonstrates how to use veracode-api-py to create a Dynamic Analysis based on simple input. There are a great many things you can do with Veracode Dynamic Analysis, including adding login and crawl scripts, defining schedules, recurrence, start/stop windows, and multiple URLs; this script does NONE of those. It simply sets up a one time scan for a single URL with credentials set via auto-login, and creates an application profile to which the results of the scan will be linked for reporting purposes.

## Setup

Clone this repository:

    git clone https://github.com/tjarrettveracode/veracode-dyn-hello-world

Install dependencies:

    cd veracode-dyn-hello-world
    pip install -r requirements.txt

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

## Run

If you have saved credentials as above you can run:

    python vcdynhello.py (arguments)

Otherwise you will need to set environment variables:

    export VERACODE_API_KEY_ID=<YOUR_API_KEY_ID>
    export VERACODE_API_KEY_SECRET=<YOUR_API_KEY_SECRET>
    python vcdynhello.py (arguments)

Arguments supported include:

* `--url`, `-u`  (required): URL to scan.
* `--username`, `-n` (opt): username to use to authenticate to the URL.
* `--password`, `-p` (required if --username is set): password to authenticate to the URL.
* `--email`, `-e` (required): email for the scan contact.
* `--business_owner`, `-b` (required): name of business owner for the scan.
* `--phone`, `-ph` (required): contact phone number for the scan.

## NOTE

1. All actions are logged to `vcdynhello.log`.
