const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn run(input: [:0]const u8) i64 {
    var safe_count: i64 = 0;
    var it = std.mem.splitScalar(u8, input, '\n');
    while (it.next()) |x| {
        var levels = std.mem.splitScalar(u8, x, ' ');
        var ascending: ?bool = null;
        var prev_value = std.fmt.parseInt(i64, levels.next().?, 10) catch unreachable;
        var safe = true;
        while (levels.next()) |y| {
            const level = std.fmt.parseInt(i64, y, 10) catch unreachable;
            if (ascending == null) {
                ascending = level >= prev_value;
            }
            if (ascending != (level >= prev_value) or @abs(level - prev_value) > 3 or level == prev_value) {
                safe = false;
                break;
            }
            prev_value = level;
        }
        if (safe) {
            safe_count += 1;
        }
    }
    return safe_count;
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
