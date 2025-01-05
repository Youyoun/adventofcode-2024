const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn is_possible(design: []const u8, patterns_array: [][]const u8, possible_array: *[]bool) bool {
    if (design.len == 0) {
        return true;
    } else if (!possible_array.*[design.len - 1]) {
        return false;
    }
    for (patterns_array) |pattern| {
        if (pattern.len > design.len) {
            continue;
        }
        if (std.mem.eql(u8, design[0..pattern.len], pattern)) {
            if (is_possible(design[pattern.len..], patterns_array, possible_array)) {
                return true;
            }
        }
    }
    possible_array.*[design.len - 1] = false;
    return false;
}

fn run(input: [:0]const u8) i64 {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    const allocator = arena.allocator();

    var it = std.mem.splitScalar(u8, input, "\n"[0]);
    const first_row = it.next().?;
    var patterns_it = std.mem.splitSequence(u8, first_row, ", ");
    var patterns_list = std.ArrayList([]const u8).init(allocator);
    while (patterns_it.next()) |pattern| {
        patterns_list.append(pattern) catch unreachable;
    }
    _ = it.next();
    var count: i64 = 0;
    while (it.next()) |design| {
        var possible_array = allocator.alloc(bool, design.len) catch unreachable;
        @memset(possible_array, true);
        if (is_possible(design, patterns_list.items, &possible_array)) {
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
