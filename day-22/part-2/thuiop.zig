const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer();

var results: [1048576]u32 = [_]u32{0} ** 1048576;
var is_done = std.bit_set.ArrayBitSet(usize, 1048576).initEmpty();

pub const ShiftInt = std.math.Log2Int(usize);

pub fn isSet(self: *std.bit_set.ArrayBitSet(usize, 1048576), index: usize) bool {
    return (self.masks[index >> @bitSizeOf(ShiftInt)] & @as(usize, 1) << @as(ShiftInt, @truncate(index))) != 0;
}

pub fn set(self: *std.bit_set.ArrayBitSet(usize, 1048576), index: usize) void {
    self.masks[index >> @bitSizeOf(ShiftInt)] |= @as(usize, 1) << @as(ShiftInt, @truncate(index));
}

fn next_secret(secret: u32) u32 {
    var temp: u32 = ((secret << 6) ^ secret) % 16777216;
    temp = ((temp >> 5) ^ temp) % 16777216;
    temp = ((temp << 11) ^ temp) % 16777216;
    return temp;
}

fn run(input: [:0]const u8) u32 {
    var it = std.mem.splitScalar(u8, input, "\n"[0]);
    std.debug.print("{any}", .{is_done.masks.len});

    while (it.next()) |row| {
        @memset(&is_done.masks, 0);
        var secret: u32 = std.fmt.parseInt(u32, row, 10) catch unreachable;
        var prev_price: i5 = @intCast(secret % 10);
        var last_4: u20 = 0;
        var i: u32 = 0;
        for (0..2000) |_| {
            secret = next_secret(secret);
            const price: i5 = @intCast(secret % 10);
            const diff: i5 = price - prev_price;
            last_4 = (last_4 << 5) + @as(u5, @bitCast(diff));
            if (i >= 4) {
                if (!isSet(&is_done, last_4)) {
                    results[last_4] += secret % 10;
                    set(&is_done, last_4);
                }
            } else {
                i += 1;
            }
            prev_price = price;
        }
    }
    return std.mem.max(u32, &results);
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
