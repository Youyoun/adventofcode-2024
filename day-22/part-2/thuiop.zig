const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer();

fn next_secret(secret: usize) usize {
    var temp: usize = ((secret * 64) ^ secret) % 16777216;
    temp = ((temp / 32) ^ temp) % 16777216;
    temp = ((temp * 2048) ^ temp) % 16777216;
    return temp;
}

fn run(input: [:0]const u8) usize {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    const allocator = arena.allocator();

    var it = std.mem.splitScalar(u8, input, "\n"[0]);

    var results = allocator.alloc(usize, 1048576) catch unreachable;
    @memset(results, 0);
    var is_done = allocator.alloc(bool, 1048576) catch unreachable;
    while (it.next()) |row| {
        @memset(is_done, false);
        var secret: usize = std.fmt.parseInt(usize, row, 10) catch unreachable;
        var prev_price: i5 = @intCast(secret % 10);
        var last_4: u20 = 0;
        var i: usize = 0;
        for (0..2000) |_| {
            secret = next_secret(secret);
            const price: i5 = @intCast(secret % 10);
            const diff: i5 = price - prev_price;
            last_4 = (last_4 << 5) + @as(u5, @bitCast(diff));
            if (i >= 4) {
                if (!is_done[last_4]) {
                    results[last_4] += secret % 10;
                    is_done[last_4] = true;
                }
            } else {
                i += 1;
            }
            prev_price = price;
        }
    }
    return std.mem.max(usize, results);
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
