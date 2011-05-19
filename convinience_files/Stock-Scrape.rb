# scrapes the stock id and stock name for entire listing on BSE website
require 'rubygems'
require 'nokogiri'
require 'open-uri'

 f = File.open('StockCodes', 'w+')
 f1 = File.open('urls', 'w+')
 alphabet = ('A'..'Z').to_a
 categories = alphabet << "[0-9]"
 ["A","B","S","T","TS","Z"].each do |letter1|
   categories.each do |letter2|
     pagecount = 1 
     while true
       ifnext = ""
       url = "http://www.bseindia.com/datalibrary/disp.asp?flag=#{letter1}&curpage=#{pagecount}&select_alp=#{letter2}"
       print url
       f1.puts(url)
       doc = Nokogiri::HTML(open(url))
       doc.search('//a[@class="class1"]').each do |link|
         #stock = link.content
         code = (/[0-9]+/.match link['href']).to_s
         stock = link.content
         #stock.concat(" ")
         #stock.concat(code)
         str = "'" + code + "', '" + stock + "'"
         f.puts(str)
       end
       doc.search('//font/a').each do |link|
         ifnext = (/Next/.match link).to_s;
         if(ifnext != "")
           f1.puts('next page found, breaking from doc search loop')
           break
         end
       end
       if(ifnext != "")
         pagecount = pagecount + 1
       else
         f1.puts('next page not  found, breaking from while loop')
         break
       end
     end
   end
 end
 f.close if f
 f1.close if f1

