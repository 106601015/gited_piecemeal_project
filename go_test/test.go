package main

import "fmt"

func main() {
    fmt.Println("Hello, World")
    chinese_hello()
}

func chinese_hello() {
	fmt.Println("哈囉！世界！")
}

//go run test.go
//go build test.go