import pandas
register = {
	"x" : [
	"x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7",
	"x8", "x9", "x10", "x11", "x12", "x13", "x14", "x15",
	"x16", "x17", "x18", "x19", "x20", "x21", "x22", "x23",
	"x24", "x25", "x26", "x27", "x28", "x29", "x30", "x31",
	],
	"name" : [
	"zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2",
	"s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5",
	"a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7",
	"s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6"
	],
	"value" : [
	"00000", "00001", "00010", "00011", "00100", "00101", "00110", "00111",
	"01000", "01001", "01010", "01011", "01100", "01101", "01110", "01111",
	"10000", "10001", "10010", "10011", "10100", "10101", "10110", "10111",
	"11000", "11001", "11010", "11011", "11100", "11101", "11110", "11111"
	]
}

regDf = pandas.DataFrame(register)