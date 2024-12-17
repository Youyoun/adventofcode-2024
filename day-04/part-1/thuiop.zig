const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn find_xmas(input: [:0]const u8) i64 {
    var xmas_count: i64 = 0;
    for (0..input.len - 3) |i| {
        if (std.mem.eql(u8, input[i .. i + 4], "XMAS") or std.mem.eql(u8, input[i .. i + 4], "SAMX")) {
            xmas_count += 1;
        }
    }
    return xmas_count;
}

fn run(input: [:0]const u8) i64 {
    const allocator = std.heap.page_allocator;
    const total_length: f32 = @floatFromInt(input.len);
    const row_length: u16 = @intFromFloat(@sqrt(total_length));

    var xmas_count: i64 = find_xmas(input);

    var copy = allocator.allocSentinel(u8, input.len, 0) catch unreachable;
    defer allocator.free(copy);

    for (0..row_length) |i| {
        for (0..row_length) |j| {
            copy[j + (row_length + 1) * i] = input[i + (row_length + 1) * j];
        }
        copy[(row_length + 1) * (i + 1) - 1] = "\n"[0];
    }
    xmas_count += find_xmas(copy);

    for (0..row_length) |i| {
        for (0..row_length) |j| {
            copy[i + (row_length + 1) * j] = input[i + (row_length + 1) * ((j + i) % row_length)];
        }
    }

    for (0..input.len - 3) |i| {
        const row = i / (row_length + 1);
        const col = i % (row_length + 1);
        if (col < row_length - row and row_length - row < col + 4) {
            continue;
        }
        if (std.mem.eql(u8, copy[i .. i + 4], "XMAS") or std.mem.eql(u8, copy[i .. i + 4], "SAMX")) {
            xmas_count += 1;
        }
    }

    for (0..row_length) |i| {
        for (0..row_length) |j| {
            copy[i + (row_length + 1) * j] = input[i + (row_length + 1) * ((j + row_length - 1 - i) % row_length)];
        }
    }
    for (0..input.len - 3) |i| {
        const row = i / (row_length + 1);
        const col = i % (row_length + 1);
        if (col < row and row < col + 4) {
            continue;
        }
        if (std.mem.eql(u8, copy[i .. i + 4], "XMAS") or std.mem.eql(u8, copy[i .. i + 4], "SAMX")) {
            xmas_count += 1;
        }
    }

    return xmas_count;
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
