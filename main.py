from aiohttp import web
import aiohttp
import asyncio
import re

loop = asyncio.get_event_loop()

routes = web.RouteTableDef()

base = 'https://discord.com'

@routes.get('/{route:.*}')
async def _get(request):
	pass
@routes.post('/{route:.*}')
async def _post(request):
	pass

website_url = 'https://discord-proxy.voltagediscordb.repl.co'
website_url_no = '//discord-proxy.voltagediscordb.repl.co'
@web.middleware
async def ocaml(request, handler):
	await handler(request)
	path = request.path
	print(path)
	if 'https://discord-proxy.voltagediscordb.repl.co' in path:
		path.replace('https://discord-proxy.voltagediscordb.repl.co','')
		url = path
	else:
	 url = base + path
	#print(url)
	method = request.method
	referer = request.headers.get('referer', base).replace(website_url, base)
	if request.body_exists:
		body = await request.read()
	else:
		body = b''
	# print(request.content_type)
	if body != b'':
		print(body)
	# print(referer)
	# print(method)
	content_type = request.content_type
	if content_type == 'application/octet-stream':
		content_type = 'text/plain'
	async with aiohttp.ClientSession(headers={'referer': referer, 'content-type': content_type}) as s:
		async with s.request(method, url, allow_redirects=False, data=body, cookies=request.cookies) as r:
			content = await r.read()
			content_type = r.content_type
			status_code = r.status
			cookies = r.cookies
			# print(status_code)
			# if status_code in {301, 302, 307}:
			# 	location = r.path
			# 	print('redirected to', location)
	if content_type.startswith('text/html'):#or content_type.startswith('application/'):
		content = content.decode()
		content = content.replace(base, website_url)
		content = content.replace('//discord.com',website_url_no)
		#content = re.sub(r'(?<=[^\/.])\bRepl\b', 'Ocaml', content)
		#content = re.sub(r'(?<=[^\/.])\brepl\b', 'ocaml', content)
		#content = content.replace(
		#	'/public/images/light-logo.svg',
		#	'http://ocaml.org/logo/Colour/SVG/colour-logo.svg'
		#)
		#content = content.replace(
                #		'/public/images/logo-small.png',
		#	'http://ocaml.org/logo/Colour/PNG/colour-logo.png'
		#)
		content = content.encode()
		
	print(cookies)
	response = web.Response(body=content, content_type=content_type, status=status_code)
	for c in cookies:
		response.cookies[str(c)] = str(cookies[c].value)
		# print('cookie name:', c)
		# print('cookie content:', cookies[c].value)
	# response.cookies = cookies
	return response


app = web.Application(middlewares=[ocaml])
app.add_routes(routes)

web.run_app(app)





# from flask import Flask, request, render_template

# app = Flask('app', static_url_path='')

 
# @app.route('/')
# def hello_world():
# return render_template('index.html')
# @app.route('/oembed')
# def oembed():
# return flask
# app.run(host='0.0.0.0', port=8080, threaded=True)