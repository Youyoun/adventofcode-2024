const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

pub const TokenType = enum {
    garbage,
    mul,
    do,
    dont,
    lparenthesis,
    rparenthesis,
    comma,
    number,
};

pub const Token = union(TokenType) {
    garbage,
    mul,
    do,
    dont,
    lparenthesis,
    rparenthesis,
    comma,
    number: i64,
};

fn tryParseMul(input: [:0]const u8, index: *usize) ?Token {
    if (index.* + 3 > input.len) return null;
    if (std.mem.eql(u8, input[index.*..][0..3], "mul")) {
        index.* += 3;
        return Token{ .mul = {} };
    } else {
        return null;
    }
}
fn tryParseDo(input: [:0]const u8, index: *usize) ?Token {
    if (index.* + 2 > input.len) return null;
    if (std.mem.eql(u8, input[index.*..][0..2], "do")) {
        index.* += 2;
        return Token{ .do = {} };
    } else {
        return null;
    }
}

fn tryParseDont(input: [:0]const u8, index: *usize) ?Token {
    if (index.* + 5 > input.len) return null;
    if (std.mem.eql(u8, input[index.*..][0..5], "don't")) {
        index.* += 5;
        return Token{ .dont = {} };
    } else {
        return null;
    }
}

fn tryParseDoOrDont(input: [:0]const u8, index: *usize) ?Token {
    if (tryParseDont(input, index)) |t| return t;
    if (tryParseDo(input, index)) |t| return t;
    return null;
}

fn isNumber(c: u8) bool {
    return '0' <= c and c <= '9';
}

fn parseNumber(input: [:0]const u8, index: *usize) Token {
    const start_index = index.*;
    while (index.* < input.len and isNumber(input[index.*])) : (index.* += 1) {}
    const number = std.fmt.parseInt(i64, input[start_index..index.*], 10) catch unreachable;
    return Token{ .number = number };
}

fn tokenize(input: [:0]const u8) []const Token {
    var index: usize = 0;
    var token_list = std.ArrayList(Token).init(a);
    while (index < input.len) {
        const c = input[index];
        switch (c) {
            'm' => {
                if (tryParseMul(input, &index)) |mul_token| {
                    token_list.append(mul_token) catch unreachable;
                } else {
                    token_list.append(Token{ .garbage = {} }) catch unreachable;
                    index += 1;
                }
            },
            'd' => {
                if (tryParseDoOrDont(input, &index)) |do_or_dont_token| {
                    token_list.append(do_or_dont_token) catch unreachable;
                } else {
                    token_list.append(Token{ .garbage = {} }) catch unreachable;
                    index += 1;
                }
            },
            '(' => {
                token_list.append(Token{ .lparenthesis = {} }) catch unreachable;
                index += 1;
            },
            ')' => {
                token_list.append(Token{ .rparenthesis = {} }) catch unreachable;
                index += 1;
            },
            ',' => {
                token_list.append(Token{ .comma = {} }) catch unreachable;
                index += 1;
            },
            '0'...'9' => {
                const token = parseNumber(input, &index);
                token_list.append(token) catch unreachable;
            },
            else => {
                token_list.append(Token{ .garbage = {} }) catch unreachable;
                index += 1;
            },
        }
    }

    return token_list.toOwnedSlice() catch unreachable;
}

fn tryParseMul2(input: []const Token, index: *usize) ?i64 {
    if (index.* + 6 > input.len) return null;
    if (input[index.*] != .mul or input[index.* + 1] != .lparenthesis or input[index.* + 2] != .number or input[index.* + 3] != .comma or input[index.* + 4] != .number or input[index.* + 5] != .rparenthesis) return null;
    defer index.* += 6;
    return input[index.* + 2].number * input[index.* + 4].number;
}

fn run(input: [:0]const u8) i64 {
    const tokens = tokenize(input);

    var index: usize = 0;
    var result: i64 = 0;
    var enabled: bool = true;
    while (index < tokens.len) {
        const token = tokens[index];
        switch (token) {
            .mul => {
                if (tryParseMul2(tokens, &index)) |v| {
                    if (enabled) {
                        result += v;
                    }
                } else {
                    index += 1;
                }
            },
            .do => {
                enabled = true;
                index += 1;
            },
            .dont => {
                enabled = false;
                index += 1;
            },
            else => index += 1,
        }
    }
    // your code here
    return result;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings

    defer arena.deinit(); // clear memory
    a = arena.allocator();

    var arg_it = try std.process.argsWithAllocator(a);
    _ = arg_it.skip(); // skip over exe name
    const input: [:0]const u8 = arg_it.next().?;

    const start: i128 = std.time.nanoTimestamp(); // start time
    const answer = run(input); // compute answer
    const end: i128 = std.time.nanoTimestamp();
    const elapsed_nano: f64 = @floatFromInt(end - start);
    const elapsed_milli = elapsed_nano / 1_000_000.0;
    try stdout.print("_duration:{d}\n{}\n", .{ elapsed_milli, answer }); // emit actual lines parsed by AOC
}

test "example" {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings

    defer arena.deinit(); // clear memory
    a = arena.allocator();

    const input =
        \\xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
    ;

    const result = run(input);
    try std.testing.expectEqual(@as(i64, 48), result);
}
