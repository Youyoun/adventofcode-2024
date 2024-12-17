const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn run(input: [:0]const u8) i64 {
    const total_length: f32 = @floatFromInt(input.len);
    const row_length: u16 = @intFromFloat(@sqrt(total_length));

    var xmas_count: i64 = 0;

    for (1..row_length) |i| {
        for (1..row_length) |j| {
            if (input[i + (row_length + 1) * j] == "A"[0]) {
                if (((input[(i - 1) + (row_length + 1) * (j - 1)] == "M"[0] and input[(i + 1) + (row_length + 1) * (j + 1)] == "S"[0]) or (input[(i - 1) + (row_length + 1) * (j - 1)] == "S"[0] and input[(i + 1) + (row_length + 1) * (j + 1)] == "M"[0])) and ((input[(i + 1) + (row_length + 1) * (j - 1)] == "M"[0] and input[(i - 1) + (row_length + 1) * (j + 1)] == "S"[0]) or (input[(i + 1) + (row_length + 1) * (j - 1)] == "S"[0] and input[(i - 1) + (row_length + 1) * (j + 1)] == "M"[0]))) {
                    xmas_count += 1;
                }
            }
        }
    }

    return xmas_count;
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
