#!/usr/bin/swift

func fibonacci(_ n: Int) -> Int {
    if n <= 2 {
        return 1
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2)
    }
}

func test_fibonacci(_ n: Int) {
    print(fibonacci(n))
}

if CommandLine.arguments.count > 1 {

  let arg = CommandLine.arguments[1] 
    if let n = Int(arg), n <= 40 {
        test_fibonacci(n)
    } else {
        print("Usage: fibonacci <n>")
    }
} else {
    print("Usage: fibonacci <n>")
}
