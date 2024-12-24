const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn next_secret(secret: usize) usize {
    var temp: usize = ((secret * 64) ^ secret) % 16777216;
    temp = ((temp / 32) ^ temp) % 16777216;
    temp = ((temp * 2048) ^ temp) % 16777216;
    return temp;
}

fn run(input: [:0]const u8) usize {
    var it = std.mem.splitScalar(u8, input, "\n"[0]);
    var result: usize = 0;
    while (it.next()) |row| {
        var secret: usize = std.fmt.parseInt(usize, row, 10) catch unreachable;
        for (0..2000) |_| {
            secret = next_secret(secret);
        }
        result += secret;
    }
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
