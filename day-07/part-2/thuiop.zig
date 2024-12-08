const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn concat(x: u64, y: u64) u64 {
    var pow: u64 = 0;
    while (std.math.pow(u64, 10, pow) <= y) {
        pow += 1;
    }
    return x * std.math.pow(u64, 10, pow) + y;
}

fn combine_recursive(number_list: []u64, i: usize, j: usize, store_array: *[]u64) u64 {
    if (j == 0) {
        return number_list[0];
    } else {
        const remainder: u64 = combine_recursive(number_list, i / 3, j - 1, store_array);
        var result: u64 = 0;
        if (i % 3 == 0) {
            result = number_list[j] + remainder;
        } else if (i % 3 == 1) {
            result = number_list[j] * remainder;
        } else {
            result = concat(remainder, number_list[j]);
        }
        //std.debug.print("rec {} {} {} {}\n", .{ i, j, result, i + j * (number_list.len - 1) });
        //store_array.*[i + (j - 1) * (number_list.len - 1)] = result;
        return result;
    }
}

fn run(input: [:0]const u8) i64 {
    const allocator = std.heap.page_allocator; // create memory allocator for strings
    var it = std.mem.splitScalar(u8, input, '\n');
    var calibration_result: u64 = 0;
    while (it.next()) |line| {
        const result_end = std.mem.indexOf(u8, line, ":").?;
        const result = std.fmt.parseInt(u64, line[0..result_end], 10) catch unreachable;
        var number_list = std.ArrayList(u64).init(allocator);
        var number_it = std.mem.splitScalar(u8, line[result_end + 2 ..], ' ');
        var length: u16 = 0;
        while (number_it.next()) |num| {
            number_list.append(std.fmt.parseInt(u64, num, 10) catch unreachable) catch unreachable;
            length += 1;
        }
        var store_array = allocator.alloc(u64, std.math.pow(u64, 3, length - 1) * (length - 1)) catch unreachable;
        @memset(store_array, 0);

        for (0..std.math.pow(u64, 3, length - 1)) |i| {
            const temp_result: u64 = combine_recursive(number_list.items, i, length - 1, &store_array);
            // std.debug.print("{} {}\n", .{ i, temp_result });

            if (temp_result == result) {
                calibration_result += result;
                break;
            }
        }
        //std.debug.print("{s}\n", .{line});
        //std.debug.print("{any}\n", .{store_array});
    }
    return @intCast(calibration_result);
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
