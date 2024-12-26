const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in
const n_iterations = 75;

fn recur(value: usize, remaining_iter: usize, results: *[n_iterations * 100]?i64) i64 {
    if (remaining_iter == 0) {
        return 1;
    }
    if (value < 100) {
        if (results.*[value + (remaining_iter - 1) * 100]) |val| {
            return val;
        }
    }
    if (value == 0) {
        const result = recur(1, remaining_iter - 1, results);
        if (value < 100) {
            results.*[value + (remaining_iter - 1) * 100] = result;
        }
        return result;
    } else {
        var pow_index: usize = 0;
        var pow: usize = 1;
        while (pow <= value) {
            pow_index += 1;
            pow *= 10;
        }
        if (pow_index % 2 == 0) {
            var half_pow: usize = 1;
            for (0..pow_index / 2) |_| {
                half_pow *= 10;
            }
            const first_part = value / half_pow;
            const second_part = value - first_part * half_pow;
            const result = recur(first_part, remaining_iter - 1, results) + recur(second_part, remaining_iter - 1, results);
            if (value < 100) {
                results.*[value + (remaining_iter - 1) * 100] = result;
            }
            return result;
        } else {
            const result = recur(value * 2024, remaining_iter - 1, results);
            if (value < 100) {
                results.*[value + (remaining_iter - 1) * 100] = result;
            }
            return result;
        }
    }
}

fn run(input: [:0]const u8) i64 {
    var it = std.mem.splitScalar(u8, input, " "[0]);
    var total: i64 = 0;
    var results: [n_iterations * 100]?i64 = undefined;
    @memset(&results, null);
    while (it.next()) |x| {
        total += recur(std.fmt.parseInt(usize, x, 10) catch unreachable, n_iterations, &results);
    }
    return total;
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
