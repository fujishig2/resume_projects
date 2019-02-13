rm -f test.s
cat common.s > test.s
cat fractal.s >> test.s
spim -f test.s
