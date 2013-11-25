import os
import requests
import json
import webbrowser

APP_ID = "YOUR_APP_ID"
APP_SECRET = "YOUR_APP_SECRET"
REDIRECT_URI = "https://www.facebook.com/connect/login_success.html"
SCOPE = "read_stream,publish_actions"

API = "https://graph.facebook.com"
FILE = "token.json"

ACCESS_TOKEN = ''

def URL(url):
	return API+url

"""https://www.facebook.com/dialog/oauth?
	client_id=396968713680793&
	redirect_uri=https://www.facebook.com/connect/login_success.html&
	response_type=token&
	scope=read_stream,publish_actions"""

def do_login():
	url = "https://www.facebook.com/dialog/oauth?client_id="+APP_ID+"&redirect_uri="+REDIRECT_URI+"&response_type=token&scope="+SCOPE
	webbrowser.open(url)

def get_access_token():
	if os.path.isfile(FILE):
		json_data = open(FILE)
		data = json.load(json_data)
		if data.has_key("access_token"):
			return data
	else:
		print """Opening url in browser. After login, copy the access token from url and enter it here."""
		do_login()
		token = raw_input()
		param = {"access_token": token}

		req = requests.get(URL('/me'),params = param)
		details = req.json()
		print(details)
		data = {"access_token": token, "id": details["id"]}
		with open(FILE,'w') as token_file:
			json.dump(data, token_file)
		return data

def do_comment(token,id,comment):
	req = requests.post(URL('/'+id+'/comments'), params = {"access_token":token,"message": comment})
	#print(req.url)
	#print(req.text)

def do_like(token,id):
	req = requests.post(URL('/'+id+'/likes?access_token='+token))
	#print(req.text)

def do_comment_and_like(token,ids):
	comment = raw_input("Enter comment to post: ")
	for id in ids:
		do_comment(token,id,comment)
		do_like(token,id)

def get_posts():
	details = get_access_token()
	url = URL('/me/feed')
	limit = raw_input("\nEnter the limit of posts to search for: ")
	payload = {"access_token" : details["access_token"], "fields": "id,message,from,type,to", "limit": limit}
	print("\nRetrieving posts...")
	req = requests.get(url, params = payload)
	data = req.json()
	if data.has_key("error"):
		print("There was an error.")
	else:
		print("\nPosts retrieved")
		search = raw_input("Enter words to search for in the messages(separate by comma (,))")
		search = search.split(',')
		print(search)
		with open("posts.json",'w') as dfile:
			json.dump(data, dfile)
		print(data)
		if data.has_key("data"):
			posts = data["data"]
			count = 1
			ids = []
			for post in posts:
				if post["type"] == "status" and post.has_key("to") and post["to"]["data"][0]["id"]==details["id"]:
					msg = post["message"].lower()
					if len(search)>0:
						for terms in search:
							if msg.find(terms) != -1:
								print(count)
								print(msg)
								ids.append(post["id"])
								count = count + 1
								break
			do_comment_and_like(details["access_token"],ids)
		else:
			print("No posts")

def show_options():
	resp = int(raw_input("1. Get Posts.\n2. Exit.\nEnter response "))
	if resp==1:
		get_posts()
	else:
		exit()

if __name__ == "__main__":
	show_options();
