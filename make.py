#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click, datetime, markdown, os, posixpath, re, string, yaml, uuid, shutil, stat, subprocess
from collections import Counter
from pprint import pprint
from jinja2 import Environment, FileSystemLoader
from typing import List
from PIL import Image


_env = Environment(loader = FileSystemLoader("./layout"))

_name = "MTG Mana Rocks"
_baseref = "https://mtgmana.rocks/"
_uuid = "0c9d723f-5560-40cc-a4c9-4d30df31e293"
_outputdir = posixpath.join(".", "docs")
_todeploy = {
	'./style/style.css': '.',
	'./style/favicon.ico': '.',
}

_assets_dir = posixpath.join(_outputdir, "assets")
_posts_dir = posixpath.join(".", "posts")

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
		"title" : _name,
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
		"title": post["title"],
		"subtitle": post.get("subtitle"),
		"author": post.get("author"),
		"date": post["date"],
		"edited": post.get("edited"),
		"banner": post.get("banner"),
		"article": post["article"],
		"permalink": post["permalink"],
		"tags": post.get("tags"),
		"previous_posts": previous_posts,
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

def deploy(target_file: str, target_dir: str, outputdir: str):
	from os.path import isfile, join, abspath

	src = abspath(target_file)
	dst = abspath(join(outputdir, target_dir))

	if isfile(src):
		copyfile(src, dst)
	else:
		dst = join(dst, os.path.basename(src))
		createdir(dst)
		for f in os.listdir(src):
			copyfile(join(src, f), join(dst, f))

def build(filter_drafts = True):
	posts = {}
	tags = Counter()

	# build post list
	for entry in os.listdir("./posts"):
		tag = os.path.splitext(entry)[0]
		post = {}

		with open(os.path.join("posts", entry), encoding="utf-8") as f:
			y, md = sum(re.findall("---(.*?)---(.*)", f.read(), re.M | re.DOTALL), ())
			post.update(yaml.safe_load(y))
			post["article"] = markdown.markdown(md, extensions=['tables', 'toc', 'fenced_code', 'admonition'])

		if filter_drafts and 'draft' in post.get('tags', []):
			continue

		post["date"] = datetime.datetime.strptime(post["date"], "%d/%m/%Y").date()
		if "edited" in post:
			post["edited"] = datetime.datetime.strptime(post["edited"], "%d/%m/%Y").date()

		post["tag"] = tag
		post["uuid"] = uuid.uuid3(uuid.NAMESPACE_DNS, tag)
		post["url"] = posixpath.join(_baseref, tag + ".html")
		post["permalink"] = posixpath.join(_baseref, post["tag"] + ".html")

		posts[tag] = post
		tags.update(post.get("tags"))

	global_vars = {
		"baseref" : _baseref,
		"keywords" : sorted([ tag[0] for tag in tags.most_common(10) ]),
	}

	# sort and filter
	sorted_list = sorted(posts.values(), key = lambda post: post["date"], reverse = True)
	sorted_list = list(sorted_list)

	# build
	for i, post in enumerate(sorted_list):
		build_post(global_vars, post, sorted_list[i+1:i+6], i == 0)
	build_index(global_vars, sorted_list[:10])
	build_archives(global_vars, sorted_list, tags)
	build_atom(global_vars, sorted_list)

	# deploy
	subprocess.call([ "sass", "--no-source-map", "./style/sass/style.scss", "./style/style.css" ])
	for target_file, target_dir in _todeploy.items():
		deploy(target_file, target_dir, _outputdir)


def list_dir(path: str, extensions: List[str]):
	for entry in os.listdir(path):

		root, ext = os.path.splitext(entry)
		if ext.lower() not in extensions:
			continue

		yield posixpath.join(path, entry)

def load_post(baseref: str, path: str):
	tag = os.path.splitext(path)[0]
	post = {
		'uuid': uuid.uuid3(uuid.NAMESPACE_DNS, tag),
		'url': posixpath.join(baseref, tag + '.html'),
	}
	with open(path, encoding='utf-8') as f:
		y, md = sum(re.findall(r'---(.*?)---(.*)', f.read(), re.M | re.DOTALL), ())

	post.update(yaml.safe_load(y))
	post['raw_article'] = md
	post['article'] = markdown.markdown(md)
	post['date'] = datetime.datetime.strptime(post['date'], '%d/%m/%Y').date()
	if 'edited' in post:
		post['edited'] = datetime.datetime.strptime(post['edited'], '%d/%m/%Y').date()

	for resource_name, resource_path in re.findall(r'\!\[(.*?)\]\((.*?)\)', post['raw_article'], re.M|re.DOTALL):
		post.setdefault('images', {})[resource_name] = resource_path

	for reference in re.findall(r'[^\!]\[(.*?)\]\[\1\]', post['raw_article'], re.M|re.DOTALL):
		post.setdefault('references', set()).add(reference)

	for link_name, link_url in re.findall(r'\[(.*?)\]\:(http.*?)$', post['raw_article'], re.M|re.DOTALL):
		post.setdefault('links', {})[link_name] = link_url

	return post

def command_optimize(assets_dir: str, max_width: int, compression_level: int, dry_run: bool):
	print(assets_dir, max_width, compression_level, dry_run)

	assets = list_dir(assets_dir, [ '.png', '.jpg', '.jpeg' ])

	for path in assets:

		print('🖼️ ', path)

		with Image.open(path) as img:
			width, height = img.size

			# Skip images that have already been optimized
			if width <= max_width:
				continue

			# Resize
			img.thumbnail((max_width, max_width))

			# Save
			if dry_run:
				root, ext = os.path.splitext(path)
				path = root + '_dry' + ext

			print('💾', path)
			img.save(path, 'JPEG', quality=compression_level)

def command_check(assets_dir: str, posts_dir: str):
	from pprint import pprint

	assets = list(list_dir(assets_dir, [ '.png', '.jpg', '.jpeg' ]))

	for path in list_dir(posts_dir, [ '.md', '.markdown' ]):
		post = load_post(_baseref, path)
		print(post['url'])
		pprint(post)
		break

@click.group()
def make():
    pass

@make.command(name='check')
def make_check():
	print('🔍', 'make_check')
	command_check(_assets_dir, _posts_dir)

@make.command(name='build')
def make_build():
	print('🏗️ ', 'make_build')

@make.command(name="optimize")
@click.option('-w', '--max-width', type=int, default=1000)
@click.option('-c', '--compression-level', type=int, default=95)
@click.option('-d', '--dry-run/--no-dry-run', default=False)
def make_optimize(max_width: int, compression_level: int, dry_run: bool):
	print('🏎️ ', 'make_optimize')
	command_optimize(_assets_dir, max_width, compression_level, dry_run)

if __name__ == '__main__':
	build(True)
