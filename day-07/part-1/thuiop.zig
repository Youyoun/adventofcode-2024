const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn combine_recursive(number_list: []i64, total: i64, target: i64) bool {
    if (number_list.len == 0) {
        return total == target;
    } else if (total > target) {
        return false;
    } else {
        return combine_recursive(number_list[1..], total + number_list[0], target) or combine_recursive(number_list[1..], total * number_list[0], target);
    }
}

fn run(input: [:0]const u8) i64 {
    const allocator = std.heap.page_allocator; // create memory allocator for strings
    var it = std.mem.splitScalar(u8, input, '\n');
    var calibration_result: i64 = 0;
    while (it.next()) |line| {
        const result_end = std.mem.indexOf(u8, line, ":").?;
        const result = std.fmt.parseInt(i64, line[0..result_end], 10) catch unreachable;
        var number_list = std.ArrayList(i64).init(allocator);
        var number_it = std.mem.splitScalar(u8, line[result_end + 2 ..], ' ');
        var length: u16 = 0;
        while (number_it.next()) |num| {
            number_list.append(std.fmt.parseInt(i64, num, 10) catch unreachable) catch unreachable;
            length += 1;
        }
        if (combine_recursive(number_list.items, 0, result)) {
            calibration_result += result;
        }
    }
    return calibration_result;
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
