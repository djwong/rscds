#!/usr/bin/awk
BEGIN {
	FS="|";
	printf("\tvar slides = [\n");
}
{
	if (substr($1, 1, 1) != "#")
		printf("\t\t{caption: \"%s\", img: \"%s\", url: \"%s\"},\n", $1, $2, $3);
}
END {
	printf("\t\t{stop: 1}\n");
	printf("\t];\n");
}
