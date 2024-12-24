const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn is_possible(design: []const u8, patterns_it: std.mem.SplitIterator(u8, std.mem.DelimiterType.sequence), possible_array: *[]?i64) i64 {
    if (design.len == 0) {
        return 1;
    } else if (possible_array.*[design.len - 1] != null) {
        return possible_array.*[design.len - 1].?;
    }
    var new_patterns_it = patterns_it;
    new_patterns_it.reset();
    var count_possible: i64 = 0;
    while (new_patterns_it.next()) |pattern| {
        if (pattern.len > design.len) {
            continue;
        }
        if (std.mem.eql(u8, design[0..pattern.len], pattern)) {
            count_possible += is_possible(design[pattern.len..], patterns_it, possible_array);
        }
    }
    possible_array.*[design.len - 1] = count_possible;
    return count_possible;
}

fn run(input: [:0]const u8) i64 {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    const allocator = arena.allocator();

    var it = std.mem.splitScalar(u8, input, "\n"[0]);
    const first_row = it.next().?;
    const patterns_it = std.mem.splitSequence(u8, first_row, ", ");
    _ = it.next();
    var count: i64 = 0;
    while (it.next()) |design| {
        var possible_array = allocator.alloc(?i64, design.len) catch unreachable;
        @memset(possible_array, null);
        count += is_possible(design, patterns_it, &possible_array);
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
