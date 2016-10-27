## bottle: (http://bottlepy.org/docs/dev/)

 Bottle은 Python을 위한, 빠르고, 간단한 경량형 WSGI(Web Server Gateway Interface) 마이크로 웹-프레임워크이다. 단일 파일 모듈로 배포되며, 다른 Python Standard Library에 대해 의존성을 지니지 않는다.

    Routing: clean, dynamic URL을 지원을 위해 매핑된 함수-호출 요청.
    Templates: 빠르고, 파이썬스러운(pythonic) 내장 템플릿엔진, mako, jinja2, cheetah 템플릿을 지원함.
    Utilities: form데이터, 파일 업로드, 쿠키, 헤더, 다른 HTTP관련 메타데이터에 접근하기 편함.
    Server: HTTP 개발서버를 내장하고 있으며, paste, fapws3, bjoern, Google App Engine, cherrypy, WSGI가 가는한 HTTP서버를 지원함.

```python
# We now try to fix 2.5/2.6/3.1/3.2 incompatibilities.
# It ain't pretty but it works... Sorry for the mess.
```

### 템플릿언어
* mako : http://www.makotemplates.org/
 - 음.. 왠지 병신같음.
* jinja2 : http://jinja.pocoo.org/docs/
 - 어디선가 본듯한 무난한 탬플릿.
* cheetah : http://www.cheetahtemplate.org/
 - 이것도 병맛.

### 참고
* clean URL : https://en.wikipedia.org/wiki/Clean_URL
* dynamic URL : http://www.webopedia.com/TERM/D/dynamic_URL.html

### ???
* Flask가 아닌 Bottle을 쓰는이유?
 - 원파일정책때문
 - Python Flask vs Bottle: http://stackoverflow.com/questions/4941145/python-flask-vs-bottle

## Primer to Asynchronous Applications
* http://bottlepy.org/docs/dev/async.html

### THE LIMIT OF SYNCHRONOUS WSGI
* WSGI specification(pep 3333): http://www.python.org/dev/peps/pep-3333/

callable한 어플리케이션은 각 request에 한번만(once) invoke되며, body iterator를 반환해야한다.

그러면 서버는 body에 대해 iterate하고, socket에 각 chunk를 써넣는다.
body의 iterator가 소멸되자마자, client 접속을 마친다.

간단하지만, snag(뜻하지 않은 문제)가 있다.
이 모든 일이 synchronously하게 이루어진다.

### GREENLETS TO THE RESCUE

thread가 process(forks)에 비해 값싸긴하지만, 새로운 connection마다 생성하기에는 여전히 값비쌈.


gevent기반 서버는
오버헤드가 거의 없이
(connection당 하나의)
수천개의 greenlet을 spawn할 수 있다.

### EVENT CALLBACK
Gevent+WSGI
1. 무한한 (pseudo)쓰래드 풀을 가지고 있기에, 새로운 connection을 받기 위해, 일직이 종료시키는 것은 이점이 없다.
2. socket을 close시키기기 위해 일직 종료시켜선 안된다(WSGI요구사항)
3. WSGI를 따라야하므로, iterable을 반환해야함.


## GeventServer
```
class ServerAdapter(object):
    quiet = False
    def __init__(self, host='127.0.0.1', port=8080, **config):
        self.options = config
        self.host = host
        self.port = int(port)

    def run(self, handler): # pragma: no cover
        pass

    def __repr__(self):
        args = ', '.join(['%s=%s'%(k,repr(v)) for k, v in self.options.items()])
        return "%s(%s)" % (self.__class__.__name__, args)


class GeventServer(ServerAdapter):
    """ Untested. Options:

        * `fast` (default: False) uses libevent's http server, but has some
          issues: No streaming, no pipelining, no SSL.
    def run(self, handler):
        from gevent import wsgi, pywsgi, local
        if not isinstance(_lctx, local.local):
            msg = "Bottle requires gevent.monkey.patch_all() (before import)"
            raise RuntimeError(msg)
        if not self.options.get('fast'): wsgi = pywsgi
        log = None if self.quiet else 'default'
        wsgi.WSGIServer((self.host, self.port), handler, log=log).serve_forever()

```
