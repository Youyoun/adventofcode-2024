const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

pub const State = enum {
    unknown,
    increasing,
    decreasing,
};

fn isReportSafeWithoutIndex(report: []const i64, index: usize) bool {
    var positive_count: usize = 0;
    var negative_count: usize = 0;
    for (report, 0..) |v, i| {
        if (i == index) continue;
        if (v == 0 or @abs(v) > 3) return false;
        if (v > 0) {
            positive_count += 1;
        } else if (v < 0) {
            negative_count += 1;
        }
    }

    return (positive_count > 0 and negative_count == 0) or (negative_count > 0 and positive_count == 0);
}

fn run(input: [:0]const u8) i64 {
    var result: i64 = 0;
    var line_it = std.mem.splitScalar(u8, input, '\n');

    var difference_list = std.ArrayList(i64).initCapacity(a, 10) catch unreachable;

    while (line_it.next()) |line| {
        var first: bool = true;
        var last: i64 = 0;

        var it = std.mem.splitScalar(u8, line, ' ');
        while (it.next()) |number_str| {
            const number = std.fmt.parseInt(i64, number_str, 10) catch unreachable;

            if (first) {
                first = false;
                last = number;
            } else {
                const diff = number - last;
                difference_list.append(diff) catch unreachable;
                last = number;
            }
        }

        for (0..difference_list.items.len) |i| {
            if (isReportSafeWithoutIndex(difference_list.items, i)) {
                result += 1;
                break;
            }
        }

        difference_list.clearRetainingCapacity();
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
test "example" {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings

    defer arena.deinit(); // clear memory
    a = arena.allocator();

    const input =
        \\7 6 4 2 1
        \\1 2 7 8 9
        \\9 7 6 2 1
        \\1 3 2 4 5
        \\8 6 4 4 1
        \\1 3 6 7 9
    ;

    const result = run(input);
    try std.testing.expectEqual(@as(i64, 2), result);
}
