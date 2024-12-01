const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

pub fn lessThan(_: void, left: i64, right: i64) bool {
    return left < right;
}

fn run(input: [:0]const u8) i64 {
    var list1 = std.ArrayList(i64).initCapacity(a, 1000) catch unreachable;
    var list2 = std.ArrayList(i64).initCapacity(a, 1000) catch unreachable;
    var it = std.mem.tokenizeAny(u8, input, "\n ");
    while (it.next()) |first_number_str| {
        const second_number_str = it.next().?;
        const first_number = std.fmt.parseInt(i64, first_number_str, 10) catch unreachable;
        const second_number = std.fmt.parseInt(i64, second_number_str, 10) catch unreachable;

        list1.append(first_number) catch unreachable;
        list2.append(second_number) catch unreachable;
    }
    std.sort.heap(i64, list1.items, {}, lessThan);
    std.sort.heap(i64, list2.items, {}, lessThan);
    var acc: i64 = 0;
    for (list1.items, list2.items) |right, left| {
        acc += @intCast(@abs(right - left));
    }
    return acc;
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
        \\3   4
        \\4   3
        \\2   5
        \\1   3
        \\3   9
        \\3   3
    ;

    const result = run(input);
    try std.testing.expectEqual(@as(i64, 11), result);
}
