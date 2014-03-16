package main

import (
    "net/http"
    "html/template"
)

func indexPageHandler(w http.ResponseWriter, r *http.Request){
    t, _ := template.ParseFiles("index.html")
    d := make(map[string]string)
    t.Execute(w, d)
}

func main() {
    http.HandleFunc("/", indexPageHandler)
    http.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.Dir("dist/"))))
    http.ListenAndServe(":8888", nil)
}
