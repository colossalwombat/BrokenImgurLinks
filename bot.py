from praw import *
import time, arrow, requests


#init variables
c_id = secret = user = pwd = message =  ""

with open("keys", 'r') as keys:
	c_id = keys.readline()[:-1]
	secret = keys.readline()[:-1]
	user = keys.readline()[:-1]
	pwd = keys.readline()[:-1]


reddit = Reddit(client_id=c_id, client_secret=secret, username=user, password=pwd, user_agent='mac:BrokenLinks0.1 (by /u/BrokenImgurLinksBot)')

subreddit = reddit.subreddit('all')

with open("logfile.txt", "a") as log:
	log.write("Successfully logged in at: " + arrow.utcnow().format("YYYY-MM-DD HH:mm:ss") + "\n")

with open("message.md", "r") as msgfile:
	message = msgfile.read()

for post in subreddit.stream.submissions():
	if not "imgur" in post.url:
		continue

	#otherwise check the page for a reddirect
	page = requests.get(post.url)


	#check the html return code
	#302 is the redirect that for imgur, always indicates the image has been removed
	if not page.history: #and page.history[0].status_code == 302:
		post.reply(message)
		print("Got one!")

		#log the reply in the file
		with open("logfile.txt", "a") as log:
			log.write("\n")
			log.write("*") * 80
			log.write("Replied to thread: " + str(post.shortlink) + " at: " + arrow.utcnow().format("YYYY-MM-DD HH:mm:ss"))

		exit()




