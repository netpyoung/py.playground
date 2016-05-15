# [Shard](http://en.wikipedia.org/wiki/Shard_%28database_architecture%29)

 database shard는 database나 search engine에서의 horizontal partition이다. 각각의 partition을 shard 혹은 database shard를 참조하게 된다.


## Database architecture

 Horizontal partitioning은 database table을 column들로 나누기(범주는 다르지만, normalization, vertical partitioning) 보다는, rows를 개별적으로 다루는(are held) database design principle이다. shard를 구성하는 각각의 partion은 database server나 물리적 장소에 위치하게 된다.

 이러한 partitioning 접근방식에는 많은 이점이 있다. table들이 나뉘고 여러개의 서버로 분배되기 때문에 각각의 database의 개별 table의 row의 전체 합은 줄어든다. 이는 주로 색인능력 향상시켜주는 index의 크기(size)를 줄여준다. database shard는 개별 hardware에 존재할 수 있으며, 여러개의 shard는 여러개의 장치에 존재할 수 있다. 이러한 것은 많은 장비에 대해 database의 분산을 가능하게 해주며, 대단한 성능 향상을 위해 여러대의 장치만큼 database 성능 폭을 넓힐수 있다는 것을 의미한다.

 Consistent hashing은, 거대 부하를 보다 작은 여러대의 서비스나, 서버로 분산시키키기 위한, 자동 sharding의 한 방법(form)이다.

## Shards compared to horizontal partitioning

Horizontal partitioning은, 보통 database 서버당 하나의 schema의 인스턴스로, 하나 혹은 이상의 table들을 row로 나누는 것이다.

Sharding은 이보다 더 나아갔다: 동일한 방식으로 문제가 있는 table들을 나누지만, schema는 여러 인스턴스가 될 수 있다. 명백한 이점으로는 크게 partition작업을 한 table의 검색 부하가, 이젠 여러 (논리적이든 물리적이든)서버로 나눠지게 된다.

Splitting shards across multiple isolated instances requires more than simple horizontal partitioning. The hoped-for gains in efficiency would be lost, if querying the database required both instances to be queried, just to retrieve a simple dimension table. Beyond partitioning, sharding thus splits large partitionable tables across the servers, while smaller tables are replicated as complete units.

This is also why sharding is related to a shared nothing architecture?once sharded, each shard can live in a totally separate logical schema instance / physical database server / data center / continent. There is no ongoing need to retain shared access (from between shards) to the other unpartitioned tables in other shards.

This makes replication across multiple servers easy (simple horizontal partitioning does not). It is also useful for worldwide distribution of applications, where communications links between data centers would otherwise be a bottleneck.

There is also a requirement for some notification and replication mechanism between schema instances, so that the unpartitioned tables remain as closely synchronized as the application demands. This is a complex choice in the architecture of sharded systems: approaches range from making these effectively read-only (updates are rare and batched), to dynamically replicated tables (at the cost of reducing some of the distribution benefits of sharding) and many options in between.


## Disadvantages of sharding

 최적화를 시키기 전에 database table을 sharding하는 것은 때아닌(premature) 복잡성을 야기시킬 수 있다.
 
 sharding은 다른 최적화 방법들이 부적합 할때 사용되야만 한다.

 database sharding의 복잡성으로 야기될 수 있는 잠재문제로는 : 
 
* SQL의 복잡도 증가 - sharding 로직을 제어하기 위해 개발자가 보다 복잡한 SQL을 작성해야 하기에, 버그가 늘어난다. 
* sharding은 복잡성을 가져왔다(introduces) - partition, balances, coordinates, ensures integrity하는 sharding 소프트웨어는 실패할 수 있다.
* 하나의 실패(Single point of failure) - network/hardwaresystem 문제로 인해, 하나의 shard에 문제가 생기면, 전체 table에 대한 실패를 야기할 수 있다.
* Failover(시스템대체작동) 서버는 더욱 복잡해진다 - Failover 서버들은 database shards의 fleats에 대한 복사본을 가지고 있어야 한다.    
* 백업이 더욱 복잡해진다 - 개별 shard에 대한 database백업은 다른 shard의 백업과 공동으로 진행되야한다(be coordinated). 
* 작동상의 복잡성도 추가된다 - index의 추가/삭제, column의 추가/삭제, schema의 수정이 더욱 어려워진다.