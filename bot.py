from praw import *
import time, arrow, requests, sys




# define the request function

def attempt(url):
	page = requests.get(post.url)

	#check the html return code
	#302 is the redirect that for imgur, always indicates the image has been removed

	try:
		if page.history and page.history[0].status_code == 302 or page.history[0].status_code == 404:
			return True
	except:
		return False

	return False

#define the reply function

def reply(post):

	post.reply(message)
	print("Got one!")

	#log the reply in the file
	with open("logfile.txt", "a") as log:
		log.write("Replied to thread: " + str(post.shortlink) + " at: " + arrow.utcnow().format("YYYY-MM-DD HH:mm:ss") + "\n")

	exit()

	return


#####################
#START OF THE SCRIPT#
#####################


#check for sufficient arguments
if len(sys.argv) < 2:
	print("USAGE: bot.py subreddit")
	exit(-1)


#init variables
c_id = secret = user = pwd = message =  ""

with open("keys", 'r') as keys:
	c_id = keys.readline()[:-1]
	secret = keys.readline()[:-1]
	user = keys.readline()[:-1]
	pwd = keys.readline()[:-1]


#log in
reddit = Reddit(client_id=c_id, client_secret=secret, username=user, password=pwd, user_agent='mac:BrokenLinks0.1 (by /u/BrokenImgurLinksBot)')

subreddit = reddit.subreddit(sys.argv[1])

with open("logfile.txt", "a") as log:
	log.write("\n\nSuccessfully logged in at: " + arrow.utcnow().format("YYYY-MM-DD HH:mm:ss") + "\n")

with open("message.md", "r") as msgfile:
	message = msgfile.read()

while True:

	for post in subreddit.new(limit=100000):

		if arrow.get(post.created_utc) < arrow.utcnow().shift(months=-6):
			continue

		if not "imgur" in post.url:
			continue

		if "m.imgur" in post.url:
			continue

		#check if the bot has already hit this post
		already_commented = False

		for comment in post.comments:
			if comment.author == "BrokenImgurLinksBot":
				already_commented = True
				break

		if already_commented:
			print("already got there")
			continue

		failures = 0

		while failures < 5:
			if attempt(post.url):
				failures += 1
				time.sleep(5)
			else:
				continue
		
		#if the loop reaches this point, 5 connection attempts have failed
		reply(post)
			



		




