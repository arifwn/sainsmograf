TODO
====

Site improvements:

- allow enlarging pictures on blog articles


Make the static site generator installable from pip

- pip install Flask-Static-Gen
- flask_static_gen create "sitename"
- created file structure:
	- config.yml
	- contents
		- pages
		- posts
	- themes
		- default
			- templates
				- layouts
					- page.html
					- post.html
				- includes
					- head.html
					- scripts.html
					- header.html
					- footer.html
				- index.html
				- posts.html
			- static
				- css
				- js
				- img
				- fonts			
