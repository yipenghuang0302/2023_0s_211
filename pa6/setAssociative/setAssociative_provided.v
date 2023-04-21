input [1:0]  read_address;

input        set_0_line_0_valid;
input        set_0_line_0_tag;
input [7:0] set_0_line_0_block;

input        set_0_line_1_valid;
input        set_0_line_1_tag;
input [7:0] set_0_line_1_block;

input        set_1_line_0_valid;
input        set_1_line_0_tag;
input [7:0] set_1_line_0_block;

input        set_1_line_1_valid;
input        set_1_line_1_tag;
input [7:0] set_1_line_1_block;

output       read_hit;
output [7:0] read_byte;

wire set_0_select;
wire set_1_select;

wire set_0_line_0_valid_select;
wire set_1_line_0_valid_select;
wire line_0_valid;

wire set_0_line_0_tag_select;
wire set_1_line_0_tag_select;
wire line_0_tag;

wire set_0_line_0_block_07_select;
wire set_0_line_0_block_06_select;
wire set_0_line_0_block_05_select;
wire set_0_line_0_block_04_select;
wire set_0_line_0_block_03_select;
wire set_0_line_0_block_02_select;
wire set_0_line_0_block_01_select;
wire set_0_line_0_block_00_select;

wire set_1_line_0_block_07_select;
wire set_1_line_0_block_06_select;
wire set_1_line_0_block_05_select;
wire set_1_line_0_block_04_select;
wire set_1_line_0_block_03_select;
wire set_1_line_0_block_02_select;
wire set_1_line_0_block_01_select;
wire set_1_line_0_block_00_select;

wire line_0_block_07;
wire line_0_block_06;
wire line_0_block_05;
wire line_0_block_04;
wire line_0_block_03;
wire line_0_block_02;
wire line_0_block_01;
wire line_0_block_00;


wire line_0_match;

wire line_0_valid_match;

wire line_0_block_07_match;
wire line_0_block_06_match;
wire line_0_block_05_match;
wire line_0_block_04_match;
wire line_0_block_03_match;
wire line_0_block_02_match;
wire line_0_block_01_match;
wire line_0_block_00_match;


wire block_07;
wire block_06;
wire block_05;
wire block_04;
wire block_03;
wire block_02;
wire block_01;
wire block_00;

assign set_0_select = ~ read_address[0];
assign set_1_select =   read_address[0];

assign set_0_line_0_valid_select = set_0_select & set_0_line_0_valid;
assign set_1_line_0_valid_select = set_1_select & set_1_line_0_valid;
assign line_0_valid = set_0_line_0_valid_select | set_1_line_0_valid_select;

assign set_0_line_0_tag_select = set_0_select & set_0_line_0_tag;
assign set_1_line_0_tag_select = set_1_select & set_1_line_0_tag;
assign line_0_tag = set_0_line_0_tag_select | set_1_line_0_tag_select;

assign set_0_line_0_block_07_select = set_0_select & set_0_line_0_block[7];
assign set_0_line_0_block_06_select = set_0_select & set_0_line_0_block[6];
assign set_0_line_0_block_05_select = set_0_select & set_0_line_0_block[5];
assign set_0_line_0_block_04_select = set_0_select & set_0_line_0_block[4];
assign set_0_line_0_block_03_select = set_0_select & set_0_line_0_block[3];
assign set_0_line_0_block_02_select = set_0_select & set_0_line_0_block[2];
assign set_0_line_0_block_01_select = set_0_select & set_0_line_0_block[1];
assign set_0_line_0_block_00_select = set_0_select & set_0_line_0_block[0];

assign set_1_line_0_block_07_select = set_1_select & set_1_line_0_block[7];
assign set_1_line_0_block_06_select = set_1_select & set_1_line_0_block[6];
assign set_1_line_0_block_05_select = set_1_select & set_1_line_0_block[5];
assign set_1_line_0_block_04_select = set_1_select & set_1_line_0_block[4];
assign set_1_line_0_block_03_select = set_1_select & set_1_line_0_block[3];
assign set_1_line_0_block_02_select = set_1_select & set_1_line_0_block[2];
assign set_1_line_0_block_01_select = set_1_select & set_1_line_0_block[1];
assign set_1_line_0_block_00_select = set_1_select & set_1_line_0_block[0];

assign line_0_block_07 = set_0_line_0_block_07_select | set_1_line_0_block_07_select;
assign line_0_block_06 = set_0_line_0_block_06_select | set_1_line_0_block_06_select;
assign line_0_block_05 = set_0_line_0_block_05_select | set_1_line_0_block_05_select;
assign line_0_block_04 = set_0_line_0_block_04_select | set_1_line_0_block_04_select;
assign line_0_block_03 = set_0_line_0_block_03_select | set_1_line_0_block_03_select;
assign line_0_block_02 = set_0_line_0_block_02_select | set_1_line_0_block_02_select;
assign line_0_block_01 = set_0_line_0_block_01_select | set_1_line_0_block_01_select;
assign line_0_block_00 = set_0_line_0_block_00_select | set_1_line_0_block_00_select;




assign line_0_match = read_address[1] ~^ line_0_tag;

assign line_0_valid_match = line_0_valid & line_0_match;

assign read_hit = line_0_valid_match | line_1_valid_match;

assign line_0_block_07_match = line_0_match & line_0_block_07;
assign line_0_block_06_match = line_0_match & line_0_block_06;
assign line_0_block_05_match = line_0_match & line_0_block_05;
assign line_0_block_04_match = line_0_match & line_0_block_04;
assign line_0_block_03_match = line_0_match & line_0_block_03;
assign line_0_block_02_match = line_0_match & line_0_block_02;
assign line_0_block_01_match = line_0_match & line_0_block_01;
assign line_0_block_00_match = line_0_match & line_0_block_00;


assign block_07 = line_0_block_07_match | line_1_block_07_match;
assign block_06 = line_0_block_06_match | line_1_block_06_match;
assign block_05 = line_0_block_05_match | line_1_block_05_match;
assign block_04 = line_0_block_04_match | line_1_block_04_match;
assign block_03 = line_0_block_03_match | line_1_block_03_match;
assign block_02 = line_0_block_02_match | line_1_block_02_match;
assign block_01 = line_0_block_01_match | line_1_block_01_match;
assign block_00 = line_0_block_00_match | line_1_block_00_match;

assign read_byte[7] = block_07;
assign read_byte[6] = block_06;
assign read_byte[5] = block_05;
assign read_byte[4] = block_04;
assign read_byte[3] = block_03;
assign read_byte[2] = block_02;
assign read_byte[1] = block_01;
assign read_byte[0] = block_00;
