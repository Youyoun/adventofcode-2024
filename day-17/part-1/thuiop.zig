const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn run(input: [:0]const u8) []usize {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings
    const allocator = arena.allocator();

    var it = std.mem.splitScalar(u8, input, "\n"[0]);
    const row_A = it.next().?;
    var reg_A: usize = std.fmt.parseInt(usize, row_A[12..row_A.len], 10) catch unreachable;
    const row_B = it.next().?;
    var reg_B: usize = std.fmt.parseInt(usize, row_B[12..row_B.len], 10) catch unreachable;
    const row_C = it.next().?;
    var reg_C: usize = std.fmt.parseInt(usize, row_C[12..row_C.len], 10) catch unreachable;
    _ = it.next();
    var it_prog = std.mem.splitScalar(u8, it.next().?[9..], ","[0]);
    var prog = std.ArrayList(u4).init(allocator);
    while (it_prog.next()) |instruction_str| {
        prog.append(std.fmt.parseInt(u4, instruction_str, 10) catch unreachable) catch unreachable;
    }
    var instruction_pointer: usize = 0;
    var output = std.ArrayList(usize).init(allocator);
    while (instruction_pointer < prog.items.len - 1) {
        const instruction = prog.items[instruction_pointer];
        const literal = prog.items[instruction_pointer + 1];
        const combo = switch (prog.items[instruction_pointer + 1]) {
            4 => reg_A,
            5 => reg_B,
            6 => reg_C,
            7 => unreachable,
            else => |x| x,
        };
        switch (instruction) {
            0 => {
                reg_A = reg_A >> @truncate(combo);
            },
            1 => {
                reg_B ^= literal;
            },
            2 => {
                reg_B = combo % 8;
            },
            3 => {
                if (reg_A != 0) {
                    instruction_pointer = literal;
                    continue;
                }
            },
            4 => {
                reg_B ^= reg_C;
            },
            5 => {
                output.append(combo % 8) catch unreachable;
            },
            6 => {
                reg_B = reg_A >> @truncate(combo);
            },
            7 => {
                reg_C = reg_A >> @truncate(combo);
            },
            else => unreachable,
        }
        instruction_pointer += 2;
    }
    return output.items;
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
    try stdout.print("_duration:{d}\n", .{elapsed_milli}); // emit actual lines parsed by AOC
    for (answer[0 .. answer.len - 1]) |value| {
        try stdout.print("{},", .{value});
    }
    try stdout.print("{}\n", .{answer[answer.len - 1]});
}
