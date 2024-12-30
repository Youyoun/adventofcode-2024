const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const Coeffs = struct {
    x: i16,
    y: i16,
};

fn parse_coeffs(str: []const u8) Coeffs {
    var it = std.mem.splitScalar(u8, str[2..], ","[0]);
    const x = std.fmt.parseInt(i16, it.next().?, 10) catch unreachable;
    const y = std.fmt.parseInt(i16, it.next().?, 10) catch unreachable;
    return Coeffs{ .x = x, .y = y };
}

fn get_quadrant(pos: Coeffs, width: usize, height: usize) ?u4 {
    if (pos.x < width / 2 and pos.y < height / 2) {
        return 0;
    } else if (pos.x > width / 2 and pos.y < height / 2) {
        return 1;
    } else if (pos.x < width / 2 and pos.y > height / 2) {
        return 2;
    } else if (pos.x > width / 2 and pos.y > height / 2) {
        return 3;
    } else {
        return null;
    }
}

fn run(input: [:0]const u8) i64 {
    var it = std.mem.splitScalar(u8, input, "\n"[0]);
    const width = 101;
    const height = 103;
    var quadrants: [4]i64 = .{0} ** 4;
    while (it.next()) |row| {
        var row_it = std.mem.splitScalar(u8, row, " "[0]);
        const pos = parse_coeffs(row_it.next().?);
        const vel = parse_coeffs(row_it.next().?);
        const final_pos = Coeffs{ .x = @mod(pos.x + 100 * vel.x, width), .y = @mod(pos.y + 100 * vel.y, height) };
        quadrants[get_quadrant(final_pos, width, height) orelse continue] += 1;
    }
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3];
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
