# require 'nokogiri'
require 'selenium-webdriver'
require 'yaml'
Selenium::WebDriver::Chrome.driver_path="./chromedriver.exe"
driver = Selenium::WebDriver.for :chrome
url='https://www.google.co.in/search?biw=1366&bih=637&tbm=isch&sa=1&ei=m-GfWq6ACYyu0gS3hrSwDA&q=smoking+scenes&oq=smoking+scenes&gs_l=psy-ab.3..0j0i24k1.29932.30515.0.30782.4.4.0.0.0.0.217.375.0j1j1.2.0....0...1c.1.64.psy-ab..2.2.375...0i7i30k1.0.lhRbfBFf3oM'
driver.navigate.to url

# driver.get("https://www.google.co.in/search?q=cigarette&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj9z5ue0Z7ZAhUHwI8KHS2zC18Q_AUICigB&biw=1366&bih=637#imgrc=e6TfIvrTmz3EaM:")
10.times{driver.execute_script("window.scrollBy(0,2000)")
	sleep(2)}

system 'mkdir', '-p', "./smoking_scenes"
no_items=driver.find_elements(:css,"div.y div.rg_bx").length
image_links=[]
puts no_items

# no_items.times { |i|
# 	driver.find_elements(:css,"div.y div.rg_bx")[i].click
# 	image_link=driver.find_elements(:css,"div.irc_land img.irc_mi")[1]["src"]
# 	puts image_link
# 	image_links<<image_link
# 	`axel -o ./cigarrettes/#{i}.jpg "#{image_link}"`

# }

(1..no_items).step(3) {
	|i|
	driver.find_elements(:css,"div.y div.rg_bx")[i].click
	3.times {
		|x|
		image_link=driver.find_elements(:css,"div.irc_land img.irc_mi")[x]["src"]
		if image_link and (image_link[-3..-1]=="png" or image_link[-3..-1]=="PNG")
			puts "PNG"
			`axel -o ./smoking_scenes/#{i}_#{x}.png "#{image_link}"`
		
		else
			`axel -o ./smoking_scenes/#{i}_#{x}.jpg "#{image_link}"`
			puts "JPG"
		end
		puts image_link
		image_links<<image_link
		File.open("./smoking_scenes_urls.txt",'w') {|f| f.write(YAML.dump(image_links))}
	} 

	puts image_links.length
}	
