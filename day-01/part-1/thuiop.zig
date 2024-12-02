const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn run(input: [:0]const u8) i64 {
    const allocator = std.heap.page_allocator; // create memory allocator for strings
    var list1 = std.ArrayList(i64).init(allocator);
    var list2 = std.ArrayList(i64).init(allocator);
    defer list1.deinit();
    defer list2.deinit();

    var it = std.mem.splitScalar(u8, input, '\n');
    while (it.next()) |x| {
        list1.append(std.fmt.parseInt(i64, x[0..5], 10) catch 0) catch std.debug.print("a", .{});
        list2.append(std.fmt.parseInt(i64, x[8..13], 10) catch 0) catch std.debug.print("b", .{});
    }
    std.mem.sort(i64, list1.items, {}, std.sort.asc(i64));
    std.mem.sort(i64, list2.items, {}, std.sort.asc(i64));
    var sum: i64 = 0;
    for (list1.items, list2.items) |x, y| {
        sum += if (x > y) x - y else y - x;
    }
    return sum;
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
