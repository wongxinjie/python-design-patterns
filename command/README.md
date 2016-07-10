##### Use cases of the Command design pattern
It is better to apply the command in the following cases:
* When you need to keep a history   of requests. An invoker can save command instances after calling its execute method to implement history functionality somewhere.
* en you need to implement callback functionality. If you pass to the nvoker two objects one after another, the second object will be a callback or the first.
* en you need requests to be handled at variant times or in variant orders.To achieve this, you can pass the command objects to different invokers, which are invoked by different conditions.
* when the invoker should be decoupled from the object handling the invocation.
*  When yoneed to implement the undo functionality. To achieve this, you need to define a method that cancels a operation performed in the execute method. For example, if you created a file, you need to delete it.

###### Advantages and disadvantages of the Command design pattern
The pros and cons of the Command design pattern are as follows:
* It is useful when creating a structure, particulary when the creating of a request and executing are not dependent on each other. It means that the Command instance can be instantiated by Client,
but run sometime later by the Invoker, and the Client and Invoker may not know anything about each other.
* This pattern helps in terms of extensibility as we can add a new command without changing the existing code.
* It allows you to create a sequence of commands named macro. To run the macro, create a list of Command instances and call the execute method of all commands.
