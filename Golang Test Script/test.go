package main

import (
	"time"

	"github.com/tebeka/selenium"
)

func main() {
	const (
		// These paths assumes that you have the selenium server and chrome driver in your PATH.
		// If not, set the absolute path to the server and driver executables.
		seleniumPath     = "selenium-server-standalone-3.141.59.jar"
		chromeDriverPath = "chromedriver"
	)

	opts := []selenium.ServiceOption{
		selenium.StartFrameBuffer(),             // Start an X frame buffer for the browser to run in.
		selenium.ChromeDriver(chromeDriverPath), // Specify the path to ChromeDriver in order to use Chrome.
	}
	selenium.SetDebug(true)
	service, err := selenium.NewSeleniumService(seleniumPath, 4444, opts...)
	if err != nil {
		panic(err) // panic is used only as an example and is not otherwise recommended.
	}
	defer service.Stop()

	// Connect to the WebDriver instance running locally.
	caps := selenium.Capabilities{
		"browserName": "chrome",
	}
	wd, err := selenium.NewRemote(caps, "http://localhost:4444/wd/hub")
	if err != nil {
		panic(err)
	}
	defer wd.Quit()

	// Navigate to the simple playground interface.
	if err := wd.Get("https://play.golang.org/"); err != nil {
		panic(err)
	}

	// Get a reference to the text box containing code.
	elem, err := wd.FindElement(selenium.ByCSSSelector, ".ace_text-input")
	if err != nil {
		panic(err)
	}

	// Enter some new code in the text box.
	if err := elem.SendKeys("package main\n\nimport \"fmt\"\n\nfunc main() {\n\tfmt.Println(\"Hello, WebDriver!\")\n}"); err != nil {
		panic(err)
	}

	// Submit the form.
	if err := elem.Submit(); err != nil {
		panic(err)
	}

	// Wait for the program to compile and run.
	time.Sleep(2 * time.Second)

	// Get the result.
	div, err := wd.FindElement(selenium.ByCSSSelector, "div.ace_line")
	if err != nil {
		panic(err)
	}
}
