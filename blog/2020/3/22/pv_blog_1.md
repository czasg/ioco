<!--
https://ae01.alicdn.com/kf/Had6f56455d994ac3af811723be80ac02F.png
java
java学习（一）
java中JDK和JRE的基础知识
java中JDK和JRE的基础知识
-->

## java学习（一）

> java中JDK和JRE的基础知识

* JDK：Java Development Kit
* JRE：Java Runtime Environment。

JRE就是运行Java字节码的虚拟机，  
如果只有Java源码，要编译成Java字节码，就需要JDK，因为JDK除了包含JRE，还提供了编译器、调试器等开发工具。

#### 基础代码
在java代码中，会定义一个类，如Hello，其中class用来表示类，public表示这个类或者方法是公开的，
而static表示静态方法，void表示该函数返回的类型，若返回为空，则指定为void即可。
```java
public class Hello{
    public static void main(String[] args){
        System.out.println("hello world");
    }
}
```
编译代码：javac Hello.java    
执行代码：java Hello  

首先用JDK编译工具将java源码编译为.class字节码，然后再用JRE运行字节码。

面向对象编程与面向过程编程。在面向过程的编程中，将一个模型拆解为一步一步的过程。而面向对象编程即
创建一个对象然后和该对象进行互动。

class的构造函数即类本身，如`public Hello(){}`  
继承类使用extends来实现`class Student extends Person`  
继承默认子类无法访问父类的private属性，但protected字段表示子类可以访问父类的private属性或方法

Overload方法是一个新方法，Override是覆写。  
多态是指，针对某个类型的方法调用，其真正执行的方法取决于运行时期实际类型的方法  
toString、equals、hashCode是三种比较重要的方法object方法

abstract，将一个类定义为抽象类，
```java
abstract class Person {
    public abstract void run();
}
```
抽象类没有字段，所有方法全部都是抽象方法。就可以把该抽象类改写为接口：interface
```java
abstract class Person {
    public abstract void run();
    public abstract String getName();
}

interface Person {
    void run();
    String getName();
}
```
当需要去实现一接口的时候，使用implements。而且一个类只能继承一个父类，但是接口可以实现多个
```java
class Student implements Person, Hello { // 实现了两个interface
    ...
}
```
static修饰的字段为静态字段，静态字段只有一个共享“空间”，所有实例都会共享该字段。  
静态方法经常用于工具类。如：Arrays.sort()等

#### String 
```java
"Hello".equals("Hello")  // 用于两个字串之间进行比较  
"Hello".contains("ll")  // 是否包含 
"Hello".indexOf("l"); // 2
"Hello".lastIndexOf("l"); // 3
"Hello".startsWith("He"); // true
"Hello".endsWith("lo"); // true
"Hello".substring(2); // "llo"
"Hello".substring(2, 4); "ll"
"\u3000Hello\u3000".strip(); // "Hello"
" Hello ".stripLeading(); // "Hello "
" Hello ".stripTrailing(); // " Hello"
"".isEmpty(); // true，因为字符串长度为0
"A,,B;C ,D".replace("ll", "~~"); // "he~~o"，所有子串"ll"被替换为"~~"
"A,,B;C ,D".replaceAll("[\\,\\;\\s]+", ","); // "A,B,C,D"
"A,B,C,D".split("\\,")

String.valueOf(123); // "123"
String.valueOf(45.67); // "45.67"
String.valueOf(true); // "true"
String.valueOf(new Object()); // 类似java.lang.Object@636be97c
```


