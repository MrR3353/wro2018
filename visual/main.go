package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
)

// home - load index.html
func home(w http.ResponseWriter, r *http.Request) {
	html, err := ioutil.ReadFile("dist/index.html")
	if err != nil {
		fmt.Print(err)
	}

	w.Write(html)
}

// defaultReceiveAjax - read data from site and change default_config
func defaultReceiveAjax(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" {
		postData := r.FormValue("sendedData")
		file, err := os.Create("config/default_config.json")
		if err != nil {
			fmt.Print(err)
		}
		w.Header().Set("Access-Control-Allow-Origin", "*")
		file.WriteString(postData)
		file.Close()
		fmt.Println("Done.")
	}
}

// receiveAjax - read data from site and change config
func receiveAjax(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" {
		postData := r.FormValue("sendedData")
		file, err := os.Create("config/config.json")
		if err != nil {
			fmt.Print(err)
		}
		w.Header().Set("Access-Control-Allow-Origin", "*")
		file.WriteString(postData)
		file.Close()
		fmt.Println("Done.")
	}
}

// sendAjax - send config to site
func sendAjax(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" {
		config, err := ioutil.ReadFile("config/config.json")
		if err != nil {
			fmt.Print(err)
		}
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Write([]byte(config))
	}
}

// sendAjax - send config to site
func sendDefaultAjax(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" {
		config, err := ioutil.ReadFile("config/default_config.json")
		if err != nil {
			fmt.Print(err)
		}
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Write([]byte(config))
	}
}

func main() {

	fmt.Println("Start ")

	http.HandleFunc("/receive_default", defaultReceiveAjax)
	http.HandleFunc("/receive", receiveAjax)
	http.HandleFunc("/send_default", sendDefaultAjax)
	http.HandleFunc("/send", sendAjax)

	http.HandleFunc("/", home)

	http.Handle("/css/", http.StripPrefix("/css/", http.FileServer(http.Dir("./dist/css/"))))
	http.Handle("/js/", http.StripPrefix("/js/", http.FileServer(http.Dir("./dist/js/"))))

	http.ListenAndServe(":8080", nil)
}
