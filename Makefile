.PHONY:all
all: out/working_group.docx out/faculty.docx

out:
	mkdir out

out/faculty.html: out parse_sitemap.py
	python3 parse_sitemap.py "Fakultätsseite" \
		"http://www.edu.tum.de/" $@

out/working_group.html: out parse_sitemap.py
	python3 parse_sitemap.py "Lehrstuhlseite" \
		"http://www.ma.edu.tum.de/" $@

%.docx: %.html
	pandoc -f html -t docx -o $@ $<
