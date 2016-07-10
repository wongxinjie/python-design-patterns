##### The use of the Proxy pattern
The Proxy pattern can be typically used when you need to extend another object's
functionalities, specifically the following:
* To control access to another object, for example, for security reasons.
* To log all calls to Subject with its parameters.
* To connect to Subject, which is located on    remote machine or another
address space. A Proxy has an interface of a remote object but also handles
the connection routine that is transparent to the caller.
* To instantiate a heavy object only when it is really needed. It can also
cache a heavy object (or part of it).
* To temporarily store some calculation results before returning to multiple
clients that can share these results.
* To count references to an object.

##### Advantagesand disadvantages of the Proxy design pattern
The main pros and cons of proxy are as follows:
* A proxy can optimize the performance of an application, using     caching of
heavy or frequently used objects.
* A proxy allows to improve the security of an application, checking access
rights in Proxy and delegating to RealSubject only if the rights are sufficient.
* Facilitating interaction between remote systems, a proxy can take over the
job of network connections and transmission routine, delegating calls to
remote objects.
* Sometimes use of the Proxy pattern can increase theresponse time from the
object. For example, if you use proxy for lazy initialization and the object
is requested for the first time, the time of the response will be increased by
initialization time
