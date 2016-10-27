logging
======================================

* http://docs.python.org/2/library/logging

Loggers:  어플리케이션 코드에서 직접 사용할 인터페이스.
Handlers: (created by loggers가 만든) log records를 적절한 목적지로 보냄.
Filters: 어떤 log records를 결과물로 남길지 결정하기 위해, 걸러내는 것.
Formatters: 최종 결과물의 log records의 layout을 명시함.


![logging_flow.png](http://docs.python.org/2/_images/logging_flow.png)



# Config
http://docs.python.org/2/library/logging.config

```logging.conf
[loggers]
keys=root,log01

[handlers]
keys=hdr01

[formatters]
keys=fmt01


[logger_root]
level= DEBUG, INFO, WARNING, ERROR, CRITICAL, NOTSET 중에 하나.
handlers= [handlers]에서 정의한 것들.

[logger_log01]
level=
handler=
propagate= 0(상위 핸들러들에게 전파하지 않음),1(상위 핸들러들에게 전파함)
qualname= logging.getLogger(qualname)에서 쓸 이름.

[handler_hdr01]
class= 핸들러 클래스이름.
level= DEBUG, INFO, WARNING, ERROR, CRITICAL, NOTSET 중에 하나.
formatter= [formatters]에서 정의한 것들.
args= logging 패키지 네임스페이스 context에서 `eval()`uate될때, handler class의 생성자인자로 들어가는 것.

[formatters_fmt01]
format= format스트링..
datefmt= 비워두거나(ISO8601 format date/times), `strftime()`에 부합한는 date/time.
class= (optional) formatter의 클래스 이름을 명시.
```

ISO8601 format example: 2003-01-23 00:29:50,411

