const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const Coeffs = struct {
    x: i16,
    y: i16,
};

fn parse_coeffs(str: []const u8) Coeffs {
    var it = std.mem.splitScalar(u8, str[2..str.len], ","[0]);
    const x = std.fmt.parseInt(i16, it.next().?, 10) catch unreachable;
    const y = std.fmt.parseInt(i16, it.next().?, 10) catch unreachable;
    return Coeffs{ .x = x, .y = y };
}

fn is_tree(robot_array: []bool, height: usize, width: usize) bool {
    var count: usize = 0;
    for (0..height - 1) |j| {
        for (0..width - 1) |i| {
            if (robot_array[i + j * width] == true) {
                count += 1;
                if (count >= 8) {
                    return true;
                }
            } else {
                count = 0;
            }
        }
    }
    return false;
}

fn run(input: [:0]const u8) i64 {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings
    defer arena.deinit(); // clear memory
    const allocator = arena.allocator();

    var it = std.mem.splitScalar(u8, input, "\n"[0]);
    const width = 101;
    const height = 103;
    var pos_list = std.ArrayList(Coeffs).init(allocator);
    var vel_list = std.ArrayList(Coeffs).init(allocator);
    while (it.next()) |row| {
        var row_it = std.mem.splitScalar(u8, row, " "[0]);
        pos_list.append(parse_coeffs(row_it.next().?)) catch unreachable;
        vel_list.append(parse_coeffs(row_it.next().?)) catch unreachable;
    }

    var i: i64 = 0;
    var robot_array = [_]bool{false} ** (width * height);
    while (true) {
        for (pos_list.items, vel_list.items) |*pos, *vel| {
            pos.x = @mod(pos.x + vel.x, width);
            pos.y = @mod(pos.y + vel.y, height);
            robot_array[@intCast(pos.x + pos.y * width)] = true;
        }
        i += 1;
        if (is_tree(&robot_array, height, width)) {
            break;
        }
        @memset(&robot_array, false);
    }
    return i;
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
