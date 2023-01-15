#!/usr/bin/swift

func fibonacci(_ n: Int) -> Int {
    if n <= 2 {
        return 1
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2)
    }
}


if CommandLine.arguments.count > 1 {

  let arg = CommandLine.arguments[1] 
    if let n = Int(arg), n <= 40 {
        print(fibonacci(n))
    } else {
        print("Usage: fibonacci <n>")
    }
} else {
    print("Usage: fibonacci <n>")
}
