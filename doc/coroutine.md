# [Coroutine](http://en.wikipedia.org/wiki/Coroutine)

coroutine은 특정 장소에서의 실행을 정지시키거나, 재시작하기 위한 다수의 entry point를 허용하는, 서브루틴을 generalize(?)한 컴퓨터 프로그램 구성요소이다.

 cooperative tasks, exceptions, event loop, infinite lists, pipes와 같은 프로그램 구성요소를 구현하기에 적합하다.

coroutine이란 용어는 Melvin Conway의 1963 논문에서 시작되었다.


"Subroutines are special cases of ... coroutines." ?Donald Knuth.

서브루틴이 invoke되면 처음(start)부터 실행되며, 종료시(finish) 한번만 빠져나간다(exit); 서브루틴 인스턴스 하나는 한번만 리턴한다.


coroutine은 비슷하지만, 기존 coroutine을 호출한 시작점을 반환하게될 다른 coroutine을 호출하며 종료(exit)될 수 있다는 점에서 (subroutine과는) 다르다; coroutine의 시각에서는 종료된 것이 아니고, 단지 또 다른 coroutine을 호출한 것일 뿐이다.



## Generator
semicoroutines 혹은 generalisation of subroutines으로 알려진, Generator는 coroutine보다 제한적이다.

둘다, 여러번 yield할 순 있지만, generator는 yield 후에 계속해서 실행을 제어할 수 없고, 대신에 제어를 generator의 caller에게 돌려준다.


top-level dispatcher routine(엄밀히 말하자면(essentially) trampoline)의 도움으로, generator로부터 돌려받은 토큰에 의해 식별할 수 있는 자식 generator에게 명시적으로 제어를 넘겨주는 방식으로, generator 기능 위에 coroutine을 구현할 수 있다.


## Thread
thread와 coroutine의 차이점은, thread는 일반적으로 선점형 스케줄인데 반해, coroutine은 그렇지 않다.

thread는 어느순간 곧 바로 스케줄이 변경될 수 있으며, 동시적으로(concurrently)실행될 수 있다.

thread를 이용하는 프로그램은 locking에 대해 조심해야 한다.

대조적으로, coroutine은 프로그램의 특정 지점에서만 스케쥴이 변경될 수 있으며 동시적으로(concurrently)실행 되지 않는다.

coroutine을 사용하는 프로그램은 보통 locking을 완전히(entirely)피할 수 있다. (이러한 속성은 event-driven 이나, asynchronous 프로그래밍에 이점으로 인용되곤 한다)


## !!!
하고나니 이미 완전 잘 번역된게 있음.. 공부했다 치자
* http://dogfeet.github.io/articles/2012/coroutine.html




## gevent: http://www.gevent.org/
 gevent는 코루틴 기반 Python 네트워킹 라이브러리이며, libevent 이벤트 루프 위에서 고-수준 synchronous API를 제공해주는 greenlet을 이용한다.
gevent -> python mysql -> pymysql -> umysql -?> mysql-connector-python

### 참고
* Comparing gevent to eventlet : http://blog.gevent.org/2010/02/27/why-gevent/
* (영) gevent For the Working Python Developer : http://sdiehl.github.io/gevent-tutorial/
* (한) Python 프로그래머를 위한 gevent 튜토리얼 : http://blog.naver.com/parkjy76/30159370760
* wiki:Monkey patch : http://en.wikipedia.org/wiki/Monkey_patch

## [greenthread](http://en.wikipedia.org/wiki/Green_threads)
* 컴퓨터 프로그래밍에서, green thread는 virtual machine에 의해 스케쥴되는 thread이다.
* green thread는 OS가 native하게 가능한지에 의존하지 않고, 멀티쓰레드 환경을 흉내낼 수 있으며, kernel space가 아닌, user space에서 관리된다.

### Performance
* 멀티코어 프로세서에서 native thread 구현체는 멀티 프로세서에 맞게 자동으로 할당되지만, green thread 구현체는 보통 그렇지 못한다.
* green thread는 몇몇 VM위에서 보다 빠르게 실행될 수 있다.
* 하지만, uniprocessor 컴퓨터에선 가장 효율적인 모델은 아직까지 정확하게 결정나지 않았다.


## [Thread pool] pattern(http://en.wikipedia.org/wiki/Thread_pool_pattern)

![threadpool](http://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Thread_pool.svg/600px-Thread_pool.svg.png)

* 컴퓨터 프로그래밍에서, thread pool pattern (replicated workers 혹은 worker-crew model)은 보통 queue에 의해 구성된 여러개의 task를 수행하기 위해 thread의 수를 정하는 것이다.
* 보통, thread보다 task가 많기에, 모든 task가 완료되기 전에 thread가 task를 완료하자 마자 queue에 다음 task를 요청한다.
* 사용되는 thread의 수가 최적의 성능을 제공하도록 튜닝할 변수로 작용될 수 있다.
* 대기 task의 수에 기반하여 동적으로 thread의 수를 바꿀 수 도 있다.
    - 많은 thread를 생성하면, 사용되지 않는 thread까지 생성함으로써 resource가 낭비될 뿐만 아니라, 시간도 소모된다.
    - 많은 thread를 죽이는 작업도 나중에 다시 생성하기 위해 많은 시간을 소비할 것이다.
    - thread를 매우 느리게 생성하는 것은 형편없는(poor) 클라이언트 성능을 야기할 것이다.
    - thread를 너무 느리게 파괴하는 것은 다른 프로세스의 리소스를 부족하게(starve) 만들것이다.
* 이러한 패턴을 구현할 때, 프로그래머는 queue의 thread-safety를 보장해주어야 한다.
* 보통, 하나의 컴퓨터에서 thread pool을 돌린다.
* 하지만, thread pool은 개념적으로 server farms와 관련있으며, thread pool자체인 master process는 전체 처리량을 늘리기 위해 다른 컴퓨터들의 worker process들에게 task를 분배하기도 한다.
* 처치 곤란 병렬 문제(Embarrassingly parallel problem)(`병렬 임무 사이의 의존성이 거의 존재하지 않거나 없는`)은 
이 방법에 매우 잘 맞아 떨어진다..

### 참고
* Connection pool
 - http://en.wikipedia.org/wiki/Connection_pool