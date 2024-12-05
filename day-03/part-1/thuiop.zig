const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn Iterator(comptime T: type) type {
    return struct {
        buffer: []const T,
        index: usize,

        const Self = @This();

        fn next(self: *Self) ?T {
            const return_val = if (self.index < self.buffer.len) self.buffer[self.index] else null;
            self.index += 1;
            return return_val;
        }

        fn peek(self: *Self) ?T {
            return if (self.index < self.buffer.len) self.buffer[self.index] else null;
        }
    };
}

fn parse_number(iterator: *Iterator(u8)) ?i64 {
    const begin_index = iterator.index;
    while (std.ascii.isDigit(iterator.peek().?)) {
        _ = iterator.next();
    }
    return std.fmt.parseInt(i64, iterator.buffer[begin_index..iterator.index], 10) catch unreachable;
}

fn parse_mul(iterator: *Iterator(u8)) ?i64 {
    if ((iterator.next() orelse return null) != "m"[0]) return null;
    if ((iterator.next() orelse return null) != "u"[0]) return null;
    if ((iterator.next() orelse return null) != "l"[0]) return null;
    if ((iterator.next() orelse return null) != "("[0]) return null;
    const n1 = parse_number(iterator) orelse return null;
    if ((iterator.next() orelse return null) != ","[0]) return null;
    const n2 = parse_number(iterator) orelse return null;
    if ((iterator.peek() orelse return null) != ")"[0]) return null;
    return n1 * n2;
}

fn run(input: [:0]const u8) i64 {
    //std.debug.print("{s}", .{input});
    var iterator: Iterator(u8) = .{ .buffer = input, .index = 0 };
    var sum: i64 = 0;
    while (iterator.peek()) |_| {
        sum += parse_mul(&iterator) orelse 0;
    }
    return sum;
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
