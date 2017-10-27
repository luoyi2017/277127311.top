def application(env, start_response):
	start_response('200 OK',[('Content-Type', 'text/html')])
	# return ['Hello world'] # Python2
	return [b'Hello world'] # Python3
