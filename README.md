mirror-me
======

mirror-me is a Slack bot that feeds on a user's message within the public channels to generate a sentence based on their word patterns and grammar to sound like them. 

mirror-me uses a basic AI technique under the hood to form these predictions using Markov chains.

Getting Started
-------

### Installation

The package includes a python virtual environment with all libraries included so there needs to be no additional installation other than the repository. 

### Usage

* Update bot.py with [GROUP_TOKEN](http://my.slack.com/services/new/bot) and [USER_TOKEN](https://api.slack.com/docs/oauth-test-tokens).

* Invite the bot to specific channels.

* Update message database using the command 'feed mirror-me' in Slack channel.

* Generate sentence using 'mirror-me' in Slack channel.

