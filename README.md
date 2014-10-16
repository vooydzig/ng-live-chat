ng-live-chat
============

Very naive implementation of live chat with bottle and angular.js It's a mix of the old school architecture and new school frameworks. Meaning no websockets and other cool(is saying 'cool' still cool?) stuff. It's just simple AJAX and polling messages every 1 second. I know it's terrible, and it for sure does NOT solve c10k problem(or any other problemfo that matter). Still it's my first take on MongoDB, bottle, angular.js AND chat app. So I guess it could be worse than it is.

Requirements
=
1. mongoDb
2. bottle.py
3. pymongo + bson
4. angular.js (uses google hosted angular.js)
