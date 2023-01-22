## [1] What is the rust statement in code?

In Rust, a statement is a line of code that performs an action or instruction. There are several types of statements in Rust, including:

Variable Declarations: Variables can be declared using the let keyword, such as let x = 5;

Expressions: Expressions are statements that evaluate to a value, such as x + y or x == y

Control Flow: Rust has several control flow statements, such as if, else, while, and for, which allow you to control the flow of execution in your code.

Function Calls: Function calls are also considered as statements and are used to invoke a function and execute the code inside it.

Return statement: The return statement is used to return a value from a function and ends the execution of the function.

### Here is an example of a Rust program that demonstrates some of these statements:

```
fn main() {
    let x = 5;
    let y = 7;
    let result = x + y;
    println!("The result is: {}", result);
    if result > 10 {
        println!("The result is greater than 10");
    } else {
        println!("The result is less than or equal to 10");
    }
    let mut i = 0;
    while i < 5 {
        println!("i is {}", i);
        i += 1;
    }
    for j in 0..5 {
        println!("j is {}", j);
    }
}

```

## [2] How to write comment in Rust?

In Rust, you can write a single line comment by using two forward slashes (//) at the beginning of the line. For example:

```
// This is a single line comment in Rust

```

You can also write a multi-line comment by using a forward slash and an asterisk (/) at the beginning of the comment, and an asterisk and a forward slash (/) at the end of the comment. For example:

```
/*
This is a
multi-line comment in Rust
*/

```

## [3] How to defined integer and float in Rust?

In Rust, you can define an integer using the i or u prefix followed by the number of bits. For example:

```
let x: i32 = 5; // x is a 32-bit signed integer
let y: u64 = 10; // y is a 64-bit unsigned integer

```

You can also define a float using the f32 or f64 prefix. For example:

```
let a: f32 = 3.14; // a is a 32-bit floating point number
let b: f64 = 2.71828; // b is a 64-bit floating point number

```

By default, Rust will infer the type of a variable based on the value you assign to it. For example:
```
let x = 5; // x is a 32-bit signed integer
let y = 3.14; // y is a 64-bit floating point number

```
You can also use the let keyword to define a variable without a type, in which case the type will be inferred:

```
let x = 5; // x is a 32-bit signed integer
let y = 3.14; // y is a 64-bit floating point number

```

You can also use the mut keyword to define a variable as mutable variable

```
let mut x = 5; // x is mutable variable
x = 10; // value of x is changed

```

## [4] How to get the type of a variable in Rust?

In Rust, you can use the std::mem::size_of function to get the size of a variable in bytes. You can also use the std::mem::size_of_val function to get the size of a variable's value, and the std::mem::align_of function to get the alignment of a variable. Here's an example of how to use these functions:

```
let x: i32 = 5;
let y: f64 = 3.14;

println!("x is {} bytes", std::mem::size_of_val(&x));
println!("y is {} bytes", std::mem::size_of_val(&y));

```
You can also use the std::any::TypeId struct to get the type of a variable at runtime, you can use the std::any::type_name function to get the name of a type. Here's an example of how to use these functions:

```
let x = 5;
let y = 3.14;
let z = "hello";

println!("x is of type {}", std::any::type_name::<decltype(x)>());
println!("y is of type {}", std::any::type_name::<decltype(y)>());
println!("z is of type {}", std::any::type_name::<decltype(z)>());

```
Note that these functions will give you the type of a variable at runtime and it's a bit different than the compile-time type, if you want to get the compile-time type of a variable you can use the std::type_name::<T>() where T is the type of the variable you want to check.
  
Note: Above code has dependency on previous version of Rust so with the newer version the following code will work for
the data type:
  
```
fn print_type_of<T>(_: &T) {
    println!("{}", std::any::type_name::<T>());
}

fn main() {
    //let a = 10;
    let mut x: i32 = 5;
    let y: i32 = 7;
    
    // let x: i32 = 10;
    x = 10;
    let result = x + y;
    println!("The result is: {}", result);
    println!("x is {} bytes", std::mem::size_of_val(&x));
    println!("result is {} bytes", std::mem::size_of_val(&result));
    print_type_of(&result);
    
    println!("---------");
    let a: f32 = 5.3;
    let b: f32 = 7.1;
    let c = a + b;
    println!("The result is: {}", c);
    println!("a is {} bytes", std::mem::size_of_val(&a));
    println!("c is {} bytes", std::mem::size_of_val(&c));
    print_type_of(&c);
}
```
## [5] How to write a function in Rust and call it? 

In Rust, you can define a function using the fn keyword, followed by the function name, a set of parentheses containing the function's parameters, an arrow (->) and the return type. Here is an example of a simple function that takes two integers as parameters and returns their sum:

```
fn add(x: i32, y: i32) -> i32 {
    x + y
}

```
You can also define function with return keyword:
```
fn add(x: i32, y: i32) -> i32 {
    return x + y;
}

```
You can call a function by using its name followed by a set of parentheses containing the function's arguments. Here's an example of how to call the add function defined above:
```
let result = add(3, 5);
println!("The sum of 3 and 5 is {}", result);
  
```
  
You can also define function with no return type, the return type of that function is () which is unit type.

```
fn print_hello() {
    println!("Hello!");
}

```
You can call the above function by simply calling the function name with parentheses:
```
print_hello();
  
```
You can also define function with default values of parameters,

```
fn add(x: i32, y: i32 = 5) -> i32 {
    x + y
}

```
You can call the above function with or without passing second parameter
```
let result = add(3);
println!("The sum of 3 and 5 is {}", result);

let result = add(3, 2);
println!("The sum of 3 and 2 is {}", result);
  
```
Functions are first-class citizens in Rust, which means you can assign them to variables, pass them as arguments to other functions, and return them from functions.


## [6] - How to get the rust compiler version from Rust Code? 

You can get the version of the Rust compiler that you are using by using the env! macro and the RUSTC environment variable. The env! macro is used to access environment variables at runtime. Here is an example of how to get the Rust compiler version:

```
fn main() {
    let rustc_version = env!("RUSTC");
    println!("The Rust compiler version is {}", rustc_version);
}

```

You can also use the std::process::Command struct to run the rustc command and get its version from the output. Here is an example of how to use std::process::Command:

```
use std::process::Command;

fn main() {
    let output = Command::new("rustc")
        .arg("--version")
        .output()
        .expect("Failed to execute process");
    let rustc_version = String::from_utf8_lossy(&output.stdout).trim();
    println!("The Rust compiler version is {}", rustc_version);
}

```
The above example, run the rustc command with --version flag and output() method of Command struct will return the Output struct. The stdout field of Output struct contains the output of the command as a byte vector. The trim() method is used to remove the leading and trailing whitespaces from the string, so that you only get the version number.

In addition, the std::version module provides the version_meta variable which contains the version metadata of the rustc version. Here is an example of how to use std::version::version_meta:

```
fn main() {
    println!("The Rust compiler version is {}", std::version::version_meta());
}

```
Please note that std::version::version_meta requires Rust 1.40.0 or later.
Note: We tested above code in 1.66.1 and it did not work as vesion method is not longer available. 


### -------------------------------------------------------------------

# Chapter 1 - Exercise Source Code:
  
```
use std::process::Command;

fn print_type_of<T>(_: &T) {
    println!("{}", std::any::type_name::<T>());
}

fn simple(){
    println!("Simple Function");
}

fn simple_add(x: i32, y: i32) -> i32{
    // let x = 10;
    // let y = 20;
    return x + y;
}

fn get_rust_version(){
    let output = Command::new("rustc")
        .arg("--version")
        .output()
        .expect("Failed to execute process");

    // Do not use the code below
    //let rustc_version = String::from_utf8_lossy(&output.stdout).trim();
    
    let binding = String::from_utf8_lossy(&output.stdout);
    let rustc_version = binding.trim();
    
    println!("The Rust compiler version is {}", rustc_version);
}

fn main() {

    // let rustc_version = env!("RUSTC");
    // println!("The Rust compiler version is {}", rustc_version);
    
    get_rust_version();
    
    
    simple();
    let sum_x_y = simple_add(10, 300);
    println!("The sum is {}", sum_x_y);
    
    print_type_of(&sum_x_y);
    /*
    let mut x: i32 = 5;
    let y: i32 = 7;
    x = 10;
    let result = x + y;
    println!("The result is: {}", result);
    println!("x is {} bytes", std::mem::size_of_val(&x));
    println!("result is {} bytes", std::mem::size_of_val(&result));
    print_type_of(&result);
    */
    
    /*
    println!("---------");
    let a: f32 = 5.3;
    let b: f32 = 7.1;
    let c = a + b;
    println!("The result is: {}", c);
    println!("a is {} bytes", std::mem::size_of_val(&a));
    println!("c is {} bytes", std::mem::size_of_val(&c));
    print_type_of(&c);
    */

    //println!("result is of type {}", std::any::type_name::<decltype(result)>());
    
    print!("Thanks");
    print!(" again.");
    /*
    if result > 10 {
        println!("The result is greater than 10");
    } else {
        println!("The result is less than or equal to 10");
    }
    let mut i = 0;
    while i < 5 {
        println!("i is {}", i);
        i += 1;
    }
    for j in 0..5 {
        println!("j is {}", j);
    }
    */
}
               
```  
