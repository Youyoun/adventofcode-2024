const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const Coeffs = struct {
    x: i64,
    y: i64,
};

fn parseRow(row: []const u8, sep: []const u8) Coeffs {
    var it = std.mem.splitScalar(u8, row, sep[0]);
    _ = it.next();
    const first_num_text = it.next().?;
    const x = std.fmt.parseInt(i64, first_num_text[0..std.mem.indexOf(u8, first_num_text, ",").?], 10) catch unreachable;
    const second_num_text = it.next().?;
    const y = std.fmt.parseInt(i64, second_num_text, 10) catch unreachable;
    return Coeffs{ .x = x, .y = y };
}

fn run(input: [:0]const u8) i64 {
    var it = std.mem.splitScalar(u8, input, "\n"[0]);

    var tokens: i64 = 0;
    while (it.next()) |A_row| {
        const B_row = it.next().?;
        const prize_row = it.next().?;
        _ = it.next();
        const coeffs_A = parseRow(A_row, "+");
        const coeffs_B = parseRow(B_row, "+");
        const prize = parseRow(prize_row, "=");
        const det = coeffs_A.x * coeffs_B.y - coeffs_B.x * coeffs_A.y;
        const num_A = coeffs_B.y * prize.x - coeffs_B.x * prize.y;
        const num_B = coeffs_A.x * prize.y - coeffs_A.y * prize.x;
        if (@mod(num_A, det) == 0 and @mod(num_B, det) == 0) {
            const number_A = @divExact(num_A, det);
            const number_B = @divExact(num_B, det);
            tokens += 3 * number_A + number_B;
        }
    }

    return tokens;
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
