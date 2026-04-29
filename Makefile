# Param default values

i := "input.xml"
o := "output.html"


convert:
	@python am_xml2html -i $(i) -o $(o)
