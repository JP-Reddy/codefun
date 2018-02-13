require 'yaml'

image_links=YAML.load_file('image_urls2.txt')
puts image_links.length
image_links.each_with_index {
	|image_link,index|
		if image_link and (image_link[-3..-1]=="png" or image_link[-3..-1]=="PNG")
			puts "PNG"
			`axel -o ./cigarrettes/#{index}.png "#{image_link}"`
		else 
			`axel -o ./cigarrettes/#{index}.jpg "#{image_link}"`
			puts "JPG"
		end
		puts image_link
}