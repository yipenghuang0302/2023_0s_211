input  [1:0] read_address;

input        set_0_valid;
input        set_0_tag;
input  [7:0] set_0_block;

input        set_1_valid;
input        set_1_tag;
input  [7:0] set_1_block;

output       read_hit;
output [7:0] read_byte;

