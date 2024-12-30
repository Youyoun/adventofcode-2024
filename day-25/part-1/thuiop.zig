const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn run(input: [:0]const u8) i64 {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings
    const allocator = arena.allocator();

    var it_schematics = std.mem.splitSequence(u8, input, "\n\n");
    var keys = std.ArrayList(u20).init(allocator);
    var locks = std.ArrayList(u20).init(allocator);
    while (it_schematics.next()) |schematic| {
        var it = std.mem.splitScalar(u8, schematic, "\n"[0]);
        var result: u20 = 0;
        while (it.next()) |row| {
            var i: u5 = 0;
            while (i < 5) : (i += 1) {
                result += @as(u20, @intFromBool(row[i] == "#"[0])) << (i * 4);
            }
        }
        var i: u5 = 0;
        while (i < 5) : (i += 1) {
            result -= @as(u20, 1) << (i * 4);
        }
        if (schematic[0] == "#"[0]) {
            locks.append(result) catch unreachable;
        } else {
            keys.append(result) catch unreachable;
        }
    }

    var count: i64 = 0;
    for (locks.items) |lock| {
        keys_loop: for (keys.items) |key| {
            var i: u5 = 0;
            while (i < 5) : (i += 1) {
                if ((lock >> (i * 4)) % 16 + (key >> (i * 4)) % 16 > 5) {
                    continue :keys_loop;
                }
            }
            count += 1;
        }
    }
    return count;
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
