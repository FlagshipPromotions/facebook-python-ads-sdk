# Copyright 2014 Facebook, Inc.

# You are hereby granted a non-exclusive, worldwide, royalty-free license to
# use, copy, modify, and distribute this software in source code or binary
# form for use in connection with the web services and APIs provided by
# Facebook.

# As with any software that integrates with the Facebook platform, your use
# of this software is subject to the Facebook Developer Principles and
# Policies [http://developers.facebook.com/policy/]. This copyright notice
# shall be included in all copies or substantial portions of the software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
import os
import sys

this_dir = os.path.dirname(__file__)
repo_dir = os.path.join(this_dir, os.pardir)
sys.path.insert(1, repo_dir)

from facebookads.objects import AdAccount, AsyncJob
from facebookads.api import FacebookAdsApi
import time
import os
import json

this_dir = os.path.dirname(__file__)
config_filename = os.path.join(this_dir, 'config.json')
config_file = open(config_filename)
config = json.load(config_file)
config_file.close()

api = FacebookAdsApi.init(access_token=config['access_token'])
account_id = config['act_id']

account = AdAccount(account_id)

# Both Insights and Reportstats
i_async_job = account.get_insights(params={'level': 'adgroup'}, async=True)
r_async_job = account.get_report_stats(
    params={
        'data_columns': ['adgroup_id'],
        'date_preset': 'last_30_days'
    },
    async=True
)

# Insights
while True:
    job = i_async_job.remote_read()
    print("Percent done: " + str(job[AsyncJob.Field.async_percent_completion]))
    time.sleep(1)
    if job:
        print "Done!"
        break

print(i_async_job.get_result())

# Reportstats
while True:
    job = r_async_job.remote_read()
    print("Percent done: " + str(job[AsyncJob.Field.async_percent_completion]))
    time.sleep(1)
    if job:
        print "Done!"
        break

print(r_async_job.get_result())
