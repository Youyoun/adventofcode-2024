const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

var ar = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings
const allocator = ar.allocator();

fn exec_program(prog: []u4, reg_A_init: usize, reg_B_init: usize, reg_C_init: usize) usize {
    var reg_A: usize = reg_A_init;
    var reg_B: usize = reg_B_init;
    var reg_C: usize = reg_C_init;
    var instruction_pointer: usize = 0;
    var output: usize = 0;
    var pow: usize = 1;
    while (instruction_pointer < prog.len - 1) {
        const instruction = prog[instruction_pointer];
        const literal = prog[instruction_pointer + 1];
        const combo = switch (prog[instruction_pointer + 1]) {
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
                output += (combo % 8) * pow;
                pow *= 8;
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
    return output;
}

fn solve(reg_A_init: usize, prog: []u4, index: usize) ?usize {
    for (0..8) |current_coeff| {
        const new_A = reg_A_init + current_coeff;
        const output = exec_program(prog, new_A, 0, 0);
        if (output % 8 == prog[index]) {
            if (index == 0) {
                return new_A;
            } else {
                return solve(8 * new_A, prog, index - 1) orelse continue;
            }
        }
    }
    return null;
}

fn run(input: [:0]const u8) usize {
    var it = std.mem.splitScalar(u8, input, "\n"[0]);
    _ = it.next();
    _ = it.next();
    _ = it.next();
    _ = it.next();
    var it_prog = std.mem.splitScalar(u8, it.next().?[9..], ","[0]);
    var prog = std.ArrayList(u4).init(allocator);
    while (it_prog.next()) |instruction_str| {
        prog.append(std.fmt.parseInt(u4, instruction_str, 10) catch unreachable) catch unreachable;
    }
    return solve(0, prog.items, prog.items.len - 1).?;
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
