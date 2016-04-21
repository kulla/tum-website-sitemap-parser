sources = out template.html parse_sitemap.py

.PHONY:all
all: out/working_group.docx out/faculty.docx

out:
	mkdir out

out/faculty.html: $(sources)
	python3 parse_sitemap.py "Fakultätsseite" \
		"http://www.edu.tum.de/" $@

out/working_group.html: $(sources)
	python3 parse_sitemap.py "Lehrstuhlseite" \
		"http://www.ma.edu.tum.de/" $@

%.docx: %.html
	pandoc -f html -t docx -o $@ $<
