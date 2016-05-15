# [Memcached](http://en.wikipedia.org/wiki/Memcached)

컴퓨팅에서,Memcashed는 범용-목적의 분산 메모리 caching 시스템이며, LibJournal를 위해 Danga Interactive사에서 개발한것이 기원이 이제는 다른 많은 사이트들이 사용하고 있다.

외부 data 소스에 대해 여러번 읽는 횟수를 줄이기 위해, RAM상에 data와 object들을 caching함으로써, 종종 동적 database-driven 웹사이트의 속도를 늘리기 위해 사용된다.

Memcached는 Unix, Linux, Windows, Mac OS X에서 동작하며, free software license하에 배포되고 있다.


## History
Brad Fitzpatrick은 그의 웹사이트 LiveJournal를 위해 May 22, 2003에 Memcached를 처음 개발했다. Anatoly Vorobey에 의해 C로 재작성되었다.

## Architecture
클라이언트-서버 구조를 이용한다.

서버는 key-value 연관 배열을 지니고 있다; 클라이언트는 이러한 배열에 상주하거나(populate) 쿼리를 날린다.

key는 250바이트를 넘을 수 있으며, value는 거의 1megabyte 정도 까지 가능하다.


클라이언트는 서버에 접속하기 전에 보통 기본포트 11211로 서비스 되는 클라이언트-사이드 라이브러리를 사용한다

 각 클라이언트들은 모든 서버에 대해 알고 있다; 서버 각각은 통신(communitate)하지 않는다.
 
 클라이언트가 특정 key에 해당하는 value를 설정/읽으려한다면, 클라이언트 라이브러리는 우선 어떤 서버를 사용할지 결정하기 위해 그 key에 대해 hash를 계산하고, 서버와 접속한다.

 서버는 그 key에 상응되는 value를 찾기 위해 두번째로 key에 대해 hash를 구한다. 서버는 RAM상에 value들을 보관하고 있다; 만약 서버가 RAM의 자원을 다 소비하면, 가장 오래된 value들이 버려지게된다.

그러므로, 클라이언트들은 Memcached를 일시적인(transitory) cache라 여기고 다뤄야 한다;


 MemcacheDB, Couchbase Server, Tarantool과 다른 database 서버들은 Memcached 프로토콜 호환성은 유지하면서, persistent storage를 제공한다.

## Security
신뢰할 수 없는 네트워크에 대해서는, SASL 인증을 지원하도록 컴파일해서 사용할 수 있다.

--------------------------------------------------------------------------------

http://www.memcached.org/about
http://code.google.com/p/memcached/wiki/NewOverview