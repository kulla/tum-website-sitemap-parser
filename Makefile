# Makefile
#
# Written in 2016 by Stephan Kulla ( http://kulla.me/ )
#
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# < http://creativecommons.org/publicdomain/zero/1.0/ >.

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
