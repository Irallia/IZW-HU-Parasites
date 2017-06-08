# node-request
`request-easy` is a thin layer ontop of Node.js http(s).request and handels all the little nasty things for you.


## options

option | default | description
----|-----|----------
retryOnError     | not set | retry the request on an Node.js error eg. req.on('error'), res.on('error')
retryOn5xx       | not set | retry the request on http 5xx status code
maxTries         | not set | limit the retries for a request with http 5xx status code; retryOn5xx has to be true
setContentLength | not set | set the `content-length` header if you provide a Buffer






## handler
    on2xx
    on3xx
    on4xx
    on5xx
    on6xx

## pass data to request
    buffer
    stream
    externalWrite
