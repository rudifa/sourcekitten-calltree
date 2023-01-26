#!/usr/bin/swift

func aaa() {
    print("aaa")

    func bbb() {
        print("bbb")
    }
    func ccc() {
        print("ccc")
        func ddd() {
            print("ddd")
        }
        ddd()
    }
    bbb()
    ccc()
}

aaa()
