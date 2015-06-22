from bs4 import BeautifulSoup
import re
import urllib2
import MySQLdb
import string

db = MySQLdb.connect("localhost","root","","mydata")
cursor = db.cursor()

flag = 0
flag2 = 0
flagparam2 = 0
flaghref1 = 0
flag_locality_list = 0
flag_city_list = 0
flag_href1 =0
print >>open ("labs_sulekha.html","w"),""
def fn (url):
	html_page = urllib2.urlopen(url)
	soup = BeautifulSoup(html_page)
	return soup


soup = BeautifulSoup(open("labs.html"))
lists = soup.find_all("div",{"class":"key-list-header"})
lab_list = lists[10].find_all("li")

lab_name = []
lab_link = []
for li in lab_list:
	lab_link.append(li.a['href'])
	lab_name.append(li.text.encode('utf-8'))
# print lab_link
# print lab_name
i=0
for item_link in lab_link:

	labname =  lab_name[i]
	i=i+1
	soupitem = fn(item_link)
	
	city_list = []
	city_listtags = soupitem.find_all("li",{"class":"loc"})

#http://yellowpages.sulekha.com/diagnostic-centers_koti_hyderabad_1
#/hyderabad/gandhi-diagnostic-centre-nallakunta-hyderabad_contact-address


########getting cities of diagnosis
	for item_citylisttags in city_listtags:
		city_list.append(item_citylisttags.text.lower().encode('utf-8'))
	print "city_list"
	print city_list
	print >>open ("labs_sulekha.html","a"),"city_list" 
	print >>open ("labs_sulekha.html","a"), city_list
	
	for item_city_list in city_list:
		print "item2"
		print item_city_list
		print >>open ("labs_sulekha.html","a"),"item2"+'\n'+str(item_city_list)
		place = item_city_list


		if item_city_list == "delhi":   #####to be changed @@@@@@@@@@@@@@@
			flag_city_list = 1
			print "Yipee! got delhi"
		elif flag_city_list == 0:
			continue

		param1 = str(item_link)+"_"+str(item_city_list)
		print param1
		print "@@@@@@@@@"
		print >>open ("labs_sulekha.html","a") ,param1 +'\n'+"@@@@@@@@@"

		soupitem2 = fn(param1)
		locality_list = []
		loclty_divtag = soupitem2.find("div",{"class":"GAQ_C_LOCALITYLINKS_T"})

		for item_loclty in loclty_divtag.find_all("a"):
			locality_list.append( "-".join(item_loclty.text.encode('utf-8').lower().replace('.',' ').replace("'",'-').split()))
		# print locality_list

		for item_locality_list in reversed(locality_list):
			# print type(item4)
			# item4 = item4.replace('.','-')
			

			#####to be changed @@@@@@@@@@@@@@@
			if item_locality_list == "pulpehladpur":
				flag_locality_list = 1
				print "Yipee! got pulpehladpur"
				print >>open ("labs_sulekha.html","a"),"Yipee! got pulpehladpur"
			elif flag_locality_list ==0:
				continue

			city = item_locality_list
			if item_locality_list =="show-less-localities":
				continue
			# print item_locality_list

			item_link = str(item_link).replace('ecg-x-ray-scan-centres','diagnostic-centers')
			# print item_link
			flagli = 0
			for num in range(1,1000):
				if flagli == 1:
					print "break"
					print >>open ("labs_sulekha.html","a"),"break"
					break
				param2 = str(item_link)+"_"+str(item_locality_list)+"_"+str(item_city_list)+"_"+str(num)
				print param2
				print >>open ("labs_sulekha.html","a"),param2

				soupitem3 = fn(param2)
				div =  soupitem3.find_all("div", {"id":"listingtabcontent"})

				for item1 in div:
					li = item1.find_all("li" , {"class":"list-item "})


					if not li:
						print "I m empty@@@@@@@@@"
						print >>open ("labs_sulekha.html","a"),"I m empty@@@@@@@@@"
						flagli = 1

					if flagli == 0:
						for a in li:
							for link in a.find_all("a", {"class":"YPTRACK GAQ_C_BUSL"}):
								href1 = link.get('href')
								soup2= fn("http://yellowpages.sulekha.com"+ href1 )
								print href1
								print >>open ("labs_sulekha.html","a"),href1

								#####to be changed @@@@@@@@@@@@@@@
								if href1 == "/delhi/sant-kripa-clinic-lab-pulpehladpur-delhi_contact-address":
									flag_href1 = 1
									print "Yipee! got href1"
									print >>open ("labs_sulekha.html","a"),"Yipee! got href1"

								if flag_href1 ==1:	

									ratingtot= soup2.find_all("div" , {"class":"span6"})
									divname = soup2.find_all("div",{"class":"pull-left"})
									divdesc = soup2.find_all("div",{"itemprop":"description"})
									lis2 = {"Link":"Not found","Link sec":"Not found","Phone/Mobile":"Not found","description":"Not found","pull-left":"Not found","Address":"Not found","Email":"Not found","Website":"Not found","Contact Person":"Not found","Working Hours":"Not found","Categories":"Not found"}
											
									#####getting overall rating info
									lisdic = {"ratingtot": "not found","review": "not found","usrrate": "not found","name": "not found","docname": "not found","link": "not found","badge": "not found"}
									
									try:
										lisdic.update({"ratingtot":ratingtot[0].text.encode('utf-8')})
									except:
										lisdic.update({"ratingtot":"Not found"})
										pass

									lisdic["ratingtot"]= MySQLdb.escape_string(str(lisdic["ratingtot"]))

									######getting badge info
									badge = soup2.find_all("div",{"class":"manage-prolink"})
									try:
										lisdic.update({"badge":badge[0].span['class'][1]})
										# print lisdic["badge"]
									except:
										lisdic.update({"badge":"Sorry !! badge not found"})

									lisdic["badge"]=MySQLdb.escape_string(str(lisdic["badge"]))


									#updating the link used in retrieving data
									lis2.update({"Link" : param2})
									lis2.update({"Link sec" : href1})

									#####for getting About info 
									try:
										if divdesc[0].p['id'] == "showmore":
											lis2.update({"description" : divdesc[0].contents[1].p.text.replace("'","\\'").encode('utf8')})
											# print divdesc[0].contents[1].p.contents[0]
										else:
											lis2.update({"description" : divdesc[0].p.text.replace("'","\\'").encode('utf8')})

											# print "About :::",divdesc[0].p.text	
									except:
										try:
											lis2.update({"description" : divdesc[0].text.replace("'","\\'").encode('utf8')})

											# print "About :::",divdesc[0].contents[0]
										except:
											lis2.update({"description" : "errrrrrrrrr1 ABOUT NOT FOUND"})

									lis2["description"] = MySQLdb.escape_string(str(lis2["description"]))

									####getting clinic name info
									try:
										lis2.update({"pull-left" : divname[0].text.replace("'","\\'").encode('utf8') })

										# print "Clinic name :::",divname[0].h1.string
									except:
										lis2.update({"pull-left" : "errrrrrrr2" })
										# print "errrrrrrr2"
									lis2["pull-left"] = MySQLdb.escape_string(str(lis2["pull-left"]))

									####getting photos
									photo = soup2.find_all("div",{"class":"row business-photos"})
									# print photo[0]#.a.img['src']
									# print "@@@@@@@@"
									# print photo[0].find_all("img")
									photolink= []
									try:
										for img in photo[0].find_all("img"):
											# print img['src']
											photolink.append(img['src'])#.replace("'","\\'"))
										# print photolink
										# photolink = MySQLdb.escape_string(str(photolink))
									except:
										photolink.append("No images found")
										# photolink = MySQLdb.escape_string(str(photolink))
										# print photolink

									photolink = MySQLdb.escape_string(str(photolink))

									

									######to find featured In of doc
									lisfeatr = []
									featured=soup2.find_all("span",{"class":"featured"})
									# print featured#.encode('utf-8')
									if featured:
										atag= featured[0].find_all("a")
										# print atag
										try:
											for a in atag:
												if(a['href']=="#prdservice"):
													featuredsm = soup2.find_all("ul",{"class":"expert-list"})
													# print featuredsm
													for a in featuredsm:
														for li_item in a.find_all("li"):
															# print li_item.text
															lisfeatr.append(li_item.text.encode('utf-8'))
													# lisfeatr = MySQLdb.escape_string(str(lisfeatr))
															# print type(lisfeatr)
															# print"@@@"
														# print lisfeatr
													break
												else:
													lisfeatr.append(a.text.encode('utf-8'))
													# lisfeatr = MySQLdb.escape_string(str(lisfeatr))
													# print a.text
										except:
											pass

										# print lisfeatr
									else:
										lisfeatr.append("Sorry!!! no featured in")
										# print lisfeatr
									
									lisfeatr = MySQLdb.escape_string(str(lisfeatr))
									# print lisfeatr




									#####getting review
									reviewlis = soup2.find_all("li" , {"class":"review-item"})
									# print reviewlis
									lisusrlis=[]
									if reviewlis:
										
										try:
											for a in reviewlis:
												usrlis=[]
												revpar = a.find_all("div",{"class":"top-review-right"})
												# print revpar[0].p.text				#review
												# print revpar[0].div.span.text		#rating
												# print revpar[0].h3.text#+'@@@@@@'+'\n'  #name
												# print "@@@@@@@@@"+'\n'
												usrlis.append(" ".join(revpar[0].p.text.split()).encode('utf-8'))
												usrlis.append(" ".join(revpar[0].div.span.text.split()).encode('utf-8'))
												usrlis.append(" ".join(revpar[0].h3.text.split()).encode('utf-8'))
												# print us)rlis
												lisusrlis.append(usrlis)
											# print lisusrlis
											# print "@@@@@@@@@@@"
											# strList = MySQLdb.escape_string(str(lisusrlis))
											# print strList
											# strList.replace('"','\\"')
											# strList.replace("'","\'")
												# print usrlis
												# print "@@@@@@"+'\n'
											# print lisusrlis
											# print "$$$$$$$"
										except:
											lisusrlis.append("SORRY!! ")
											# print lisusrlis
									else:
										lisusrlis.append("SORRY!! no reviews were found ")
										# print lisusrlis

									strList = MySQLdb.escape_string(str(lisusrlis))


									#####getting phone,website,contact,email etc
									div2 = soup2.find_all("div",{"class":"profile-list"})
									for item in div2:
										 li2 = item.find_all("li",{"class":"row"})
										 for item2 in li2:
										 	dv1= item2.find_all("div",{"class":"profile-details"})
										 	dv2=item2.find_all("div",{"class":"profile-child"})
										 	
										 	for a in dv1:
										 		# print a.strong.text," ::: ", a.div.text
										 		try:
										 			lis2.update({a.strong.text.replace("'","\\'").encode('utf8') : " ".join(a.div.text.split()).replace("'","\\'").encode('utf8') })


										 		except:
										 			lis2.update({a.strong.text.replace("'","\\'").encode('utf8') : "err bro"})


									lis2["Phone/Mobile"] = MySQLdb.escape_string(str(lis2["Phone/Mobile"]))
									lis2["Address"] = MySQLdb.escape_string(str(lis2["Address"]))
									lis2["Email"] = MySQLdb.escape_string(str(lis2["Email"]))
									lis2["Website"] = MySQLdb.escape_string(str(lis2["Website"]))
									lis2["Contact Person"] = MySQLdb.escape_string(str(lis2["Contact Person"]))
									lis2["Working Hours"] = MySQLdb.escape_string(str(lis2["Working Hours"]))
									lis2["Categories"] = MySQLdb.escape_string(str(lis2["Categories"]))

									lis2.update({"state":place})
									lis2.update({"labname":labname})
									# print lis2['state']

									sql = "INSERT INTO `labs_sulekha`(`Phone`, `Address`, `Email`, `Website`, `Contact Person`, `Working hrs`, `Categories`,`About`, `Clinic name`, `Link`, `Link sec`, `City`,`Badge`, `Photoslink`, `Reviews`, `Featuredin`, `RatingTot`,`State`,`Labname`) VALUES (" +'"' +lis2["Phone/Mobile"]+'"'+',"'+lis2["Address"]+'"'+',"'+lis2["Email"]+'"'+',"'+lis2["Website"]+'"'+',"'+lis2["Contact Person"]+'"'+',"'+lis2["Working Hours"]+'"'+',"'+lis2["Categories"]+'"'+',"'+lis2["description"]+'"'+',"'+lis2["pull-left"]+'"'+',"'+lis2["Link"]+'"'+',"'+lis2["Link sec"]+'"'+',"'+city+'"'+',"'+lisdic["badge"]+'"'+',"'+str(photolink)+'"'+',"'+str(strList)+'"'+',"'+str(lisfeatr)+'"'+',"'+lisdic["ratingtot"]+'"'+',"'+lis2["state"]+'"'+',"'+lis2["labname"]+'"'+ ")"

									# print sql
									cursor.execute(sql)
									db.commit()
									# print lis2["Link"]
									# print lis2["Link sec"]
										 		# f.write( str(a.strong.text)+" ::: " +str(a.div.text))
									print "########@@@@@@#####"
									print >>open ("labs_sulekha.html","a"),"########@@@@@@#####"

