package main

import (
    "bufio"
    "fmt"
    "os"
    "strconv"
    "strings"
)

func main() {
    if len(os.Args) != 2 {
        fmt.Println("Usage:", os.Args[0], "INPUTFILE")
        return
    }
    filename := os.Args[1]
    file, err := os.Open(filename)
    if err != nil {
        panic(err)
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)

    horizontal := 0
    depth := 0

    aim2 := 0
    horizontal2 := 0
    depth2 := 0

    for scanner.Scan() {
        tokens := strings.Fields(scanner.Text())
        direction := tokens[0]
        value, _ := strconv.Atoi(tokens[1])
        if direction == "forward" {
            horizontal += value
            horizontal2 += value
            depth2 += aim2 * value
        } else if direction == "up" {
            depth -= value
            aim2 -= value
        } else if direction == "down" {
            depth += value
            aim2 += value
        }
    }

    fmt.Println(horizontal * depth)
    fmt.Println(horizontal2 * depth2)
}
