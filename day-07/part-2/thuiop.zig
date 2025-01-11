const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

var number_list = [_]u64{0} ** 15;

fn parseInt(comptime T: type, str: []const u8) T {
    var result: T = 0;
    for (str) |char| {
        result *= 10;
        result += char - 48;
    }
    return result;
}

fn truncate(x: u64, y: u64) ?u64 {
    var pow: u64 = 10;
    while (pow <= y) {
        pow *= 10;
    }
    const diff = x - y;
    const div = diff / pow;
    if (diff - (div) * pow == 0) {
        return div;
    }
    return null;
}

fn combine_recursive(numbers: []u64, target: u64) bool {
    if (numbers.len == 0) {
        return target == 0;
    } else if (target < numbers[0]) {
        return false;
    } else {
        if (combine_recursive(numbers[1..], target - numbers[0])) {
            return true;
        }
        const div = target / numbers[0];
        if (target - div * numbers[0] == 0) {
            if (combine_recursive(numbers[1..], div)) {
                return true;
            }
        }
        if (truncate(target, numbers[0])) |new_target| {
            if (combine_recursive(numbers[1..], new_target)) {
                return true;
            }
        }
        return false;
    }
}

fn run(input: [:0]const u8) u64 {
    var it = std.mem.splitScalar(u8, input, '\n');
    var calibration_result: u64 = 0;
    var length: u16 = 0;
    while (it.next()) |line| {
        length = 0;
        const result_end = std.mem.indexOf(u8, line, ":").?;
        const result = parseInt(u64, line[0..result_end]);
        var number_it = std.mem.splitBackwardsScalar(u8, line[result_end + 2 ..], ' ');
        while (number_it.next()) |num| {
            number_list[length] = parseInt(u64, num);
            length += 1;
        }
        if (combine_recursive(number_list[0..length], result)) {
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
    for (0..100) |_| {
        _ = run(input); // compute answer
    }
    const end: i128 = std.time.nanoTimestamp();
    const answer = run(input); // compute answer
    const elapsed_nano: f64 = @floatFromInt(end - start);
    const elapsed_milli = elapsed_nano / 1_000_000.0 / 100;
    try stdout.print("_duration:{d}\n{}\n", .{ elapsed_milli, answer }); // emit actual lines parsed by AOC
}
