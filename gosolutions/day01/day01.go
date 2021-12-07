package main

import (
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
    data, err := os.ReadFile(filename)
    if err != nil {
        panic(err)
    }
    dataString := string(data)
    depthStrings := strings.Fields(dataString)
    size := len(depthStrings)
    depthInts := make([]int, size)
    for i, s := range depthStrings {
        intified, _ := strconv.Atoi(s)
        depthInts[i] = intified
    }

    partOneCount := 0
    for i := 1; i < len(depthInts); i++ {
        if depthInts[i] > depthInts[i - 1] { partOneCount++ }
    }
    fmt.Println(partOneCount)

    partTwoCount := 0
    for i := 3; i < len(depthInts); i++ {
        if depthInts[i] > depthInts[i - 3] { partTwoCount++ }
    }
    fmt.Println(partTwoCount)
}
