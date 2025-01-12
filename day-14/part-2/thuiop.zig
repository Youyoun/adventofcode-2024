const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const width = 101;
const height = 103;
const bitset_type = std.bit_set.ArrayBitSet(u32, width * height);
var robot_array = bitset_type.initEmpty();

pub const ShiftInt = std.math.Log2Int(u32);

pub fn isSet(self: *bitset_type, index: usize) bool {
    return (self.masks[index >> @bitSizeOf(ShiftInt)] & @as(u32, 1) << @as(ShiftInt, @truncate(index))) != 0;
}

pub fn set(self: *bitset_type, index: usize) void {
    self.masks[index >> @bitSizeOf(ShiftInt)] |= @as(u32, 1) << @as(ShiftInt, @truncate(index));
}

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

fn is_tree() bool {
    for (robot_array.masks) |mask| {
        if (@popCount(mask) >= 22) {
            return true;
        }
    }
    return false;
}

fn run(input: [:0]const u8) i64 {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings
    const allocator = arena.allocator();

    var it = std.mem.splitScalar(u8, input, "\n"[0]);
    var pos_x_list = std.ArrayList(i16).init(allocator);
    var vel_x_list = std.ArrayList(i16).init(allocator);
    var pos_y_list = std.ArrayList(i16).init(allocator);
    var vel_y_list = std.ArrayList(i16).init(allocator);
    while (it.next()) |row| {
        var row_it = std.mem.splitScalar(u8, row, " "[0]);
        const coeffs_pos = parse_coeffs(row_it.next().?);
        const coeffs_vel = parse_coeffs(row_it.next().?);
        pos_x_list.append(coeffs_pos.x) catch unreachable;
        pos_y_list.append(coeffs_pos.y) catch unreachable;
        vel_x_list.append(coeffs_vel.x) catch unreachable;
        vel_y_list.append(coeffs_vel.y) catch unreachable;
    }

    const pos_x = pos_x_list.items;
    const pos_y = pos_y_list.items;
    const vel_x = vel_x_list.items;
    const vel_y = vel_y_list.items;

    var count: i64 = 0;
    while (true) {
        for (0..pos_x.len) |i| {
            pos_x[i] += vel_x[i];
            pos_y[i] += vel_y[i];
            pos_x[i] = @mod(pos_x[i], width);
            pos_y[i] = @mod(pos_y[i], height);
        }
        for (0..pos_x.len) |i| {
            set(&robot_array, @intCast(pos_x[i] + pos_y[i] * width));
        }
        count += 1;
        if (is_tree()) {
            break;
        }
        @memset(&robot_array.masks, 0);
    }
    return count;
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
