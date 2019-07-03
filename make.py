#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, markdown, os, posixpath, re, string, yaml, uuid, shutil, stat, subprocess
from collections import Counter
from pprint import pprint
from jinja2 import Environment, FileSystemLoader

_env = Environment(loader = FileSystemLoader("./layout"))

_baseref = "http://mtgmana.rocks/"
_uuid = "0c9d723f-5560-40cc-a4c9-4d30df31e293"
_outputdir = posixpath.join(".", "docs")
_todeploy = [ "./style/style.css", "./style/prettify/" ]

def createdir(dirname):
	if not os.path.exists(dirname):
		os.makedirs(dirname, 0o700)

def render(target_name, template_name, context):
	fullpath = posixpath.join(_outputdir, target_name)
	createdir(_outputdir)
	with open(fullpath, 'w', encoding="utf-8") as f:
		content = _env.get_template(template_name).render(context)
		f.write(content)
	os.chmod(fullpath, stat.S_IREAD|stat.S_IWRITE)

def build_atom(global_vars, posts):
	context = {
		"uuid" : _uuid,
		"date" : datetime.datetime.today(),
		"entries" : [post for post in posts if "draft" not in post.get("tags", [])],
	}
	context.update(global_vars)
	render("feed.atom", "feed.atom", context)

def build_archives(global_vars, posts, tags):
	tag_list = [ (tag[0], [ post for post in posts if tag[0] in post.get("tags", []) ]) for tag in tags.most_common() ]
	tag_list = filter(lambda x: len(x[1]), tag_list)

	context = {
		"title" : "Complete archives",
		"posts" : posts,
		"tag_list" : tag_list,
	}
	context.update(global_vars)
	render("archives.html", "archives.html", context)

def build_post(global_vars, post, previous_posts, is_first = False):
	context = {
		"title" : post["title"],
		"subtitle" : post.get("subtitle"),
		"author" : post.get("author"),
		"date" : post["date"],
		"edited" : post.get("edited"),
		"article" : post["article"],
		"permalink" : posixpath.join(_baseref, post["tag"] + ".html"),
		"tags" : post.get("tags"),
		"previous_posts" : previous_posts,
	}
	context.update(global_vars)
	render(post["tag"] + ".html", "post.html", context)

def build_index(global_vars, posts):
	context = {
		"title" : "MTG Mana Rocks",
		"posts" : posts,
	}
	context.update(global_vars)
	render("index.html", "index.html", context)

def copyfile(src, dst):
	createdir(os.path.dirname(dst))
	shutil.copy(src, dst)

def deploy(src, dst):
	from os.path import isfile, join, abspath

	src = abspath(src)
	dst = abspath(dst)

	if isfile(src):
		copyfile(src, dst)
	else:
		dst = join(dst, os.path.basename(src))
		createdir(dst)
		for f in os.listdir(src):
			copyfile(join(src, f), join(dst, f))

def main(filter_drafts = True):
	posts = {}
	tags = Counter()

	# build post list
	for entry in os.listdir("./posts"):
		tag = os.path.splitext(entry)[0]
		post = posts.setdefault(tag, {})

		with open(os.path.join("posts", entry), encoding="utf-8") as f:
			y, md = sum(re.findall("---(.*?)---(.*)", f.read(), re.M | re.DOTALL), ())
			post.update(yaml.safe_load(y))
			post["article"] = markdown.markdown(md)

		post["date"] = datetime.datetime.strptime(post["date"], "%d/%m/%Y").date()
		if "edited" in post:
			post["edited"] = datetime.datetime.strptime(post["edited"], "%d/%m/%Y").date()

		tags.update(post.get("tags"))

		post["tag"] = tag
		post["uuid"] = uuid.uuid3(uuid.NAMESPACE_DNS, tag)
		post["url"] = posixpath.join(_baseref, tag + ".html")

	global_vars = {
		"baseref" : _baseref,
		"keywords" : [ tag[0] for tag in tags.most_common(10) ],
	}

	# sort and filter
	sorted_list = sorted(posts.values(), key = lambda post: post["date"], reverse = True)
	if filter_drafts:
		sorted_list = filter(lambda p: not 'draft' in p['tags'], sorted_list)
	sorted_list = list(sorted_list)

	# build
	build_index(global_vars, sorted_list[:10])

	for i, post in enumerate(sorted_list):
		build_post(global_vars, post, sorted_list[i+1:i+6], i == 0)

	build_archives(global_vars, sorted_list, tags)
	build_atom(global_vars, sorted_list)

	# deploy
	subprocess.call([ "sass", "./style/sass/style.scss", "./style/style.css" ])
	for target in _todeploy:
		deploy(target, _outputdir)

if __name__ == "__main__":
	main(False)
