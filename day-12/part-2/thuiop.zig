const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const RegionPair = struct {
    first_region: usize,
    second_region: usize,
};

const CheckResultTag = enum {
    region_pair,
    region_num,
    no_region,
};

const CheckResult = union(CheckResultTag) {
    region_pair: RegionPair,
    region_num: usize,
    no_region: void,
};

const Position = struct {
    i: usize,
    j: usize,

    fn is_not_out(pos: Position, length: usize) bool {
        return pos.i >= 0 and pos.i <= length - 1 and pos.j >= 0 and pos.j <= length - 1;
    }

    fn get_val(pos: Position, comptime T: type, array: []T, row_length: usize) T {
        return array[pos.i + pos.j * row_length];
    }

    fn set_val(pos: Position, comptime T: type, value: T, array: *[]T, row_length: usize) void {
        array.*[pos.i + pos.j * row_length] = value;
    }

    fn check_before(pos: Position, field_array: []const u8, region_array: []?usize, row_length: usize) CheckResult {
        const current_val = field_array[pos.i + pos.j * row_length];

        if (pos.i > 0 and pos.j > 0 and field_array[pos.i - 1 + pos.j * row_length] == current_val and field_array[pos.i + (pos.j - 1) * row_length] == current_val) {
            const left_region = region_array[pos.i - 1 + pos.j * row_length].?;
            const up_region = region_array[pos.i + (pos.j - 1) * row_length].?;
            if (left_region != up_region) {
                return CheckResult{ .region_pair = RegionPair{ .first_region = left_region, .second_region = up_region } };
            } else {
                return CheckResult{ .region_num = left_region };
            }
        } else if (pos.i > 0 and field_array[pos.i - 1 + pos.j * row_length] == current_val) {
            const left_region = region_array[pos.i - 1 + pos.j * row_length].?;
            return CheckResult{ .region_num = left_region };
        } else if (pos.j > 0 and field_array[pos.i + (pos.j - 1) * row_length] == current_val) {
            const up_region = region_array[pos.i + (pos.j - 1) * row_length].?;
            return CheckResult{ .region_num = up_region };
        } else {
            return CheckResult.no_region;
        }
    }

    fn get_perimeter(pos: Position, field_array: []const u8, row_length: usize) i64 {
        const current_val = field_array[pos.i + pos.j * row_length];
        var perimeter: i64 = 0;
        if ((pos.i == 0) or (field_array[pos.i - 1 + pos.j * row_length] != current_val)) {
            const prev_pos = Position{ .i = pos.i, .j = pos.j - 1 };
            const prev_val = field_array[prev_pos.i + prev_pos.j * row_length];
            if (pos.j == 0 or !(prev_val == current_val and ((prev_pos.i == 0) or (field_array[prev_pos.i - 1 + prev_pos.j * row_length] != current_val)))) {
                perimeter += 1;
            }
        }
        if ((pos.i == row_length - 2) or (field_array[pos.i + 1 + pos.j * row_length] != current_val)) {
            const prev_pos = Position{ .i = pos.i, .j = pos.j - 1 };
            const prev_val = field_array[prev_pos.i + prev_pos.j * row_length];
            if (pos.j == 0 or !(prev_val == current_val and ((prev_pos.i == row_length - 2) or (field_array[prev_pos.i + 1 + prev_pos.j * row_length] != current_val)))) {
                perimeter += 1;
            }
        }
        if ((pos.j == 0) or (field_array[pos.i + (pos.j - 1) * row_length] != current_val)) {
            const prev_pos = Position{ .i = pos.i - 1, .j = pos.j };
            const prev_val = field_array[prev_pos.i + prev_pos.j * row_length];
            if (pos.i == 0 or !(prev_val == current_val and ((prev_pos.j == 0) or (field_array[prev_pos.i + (prev_pos.j - 1) * row_length] != current_val)))) {
                perimeter += 1;
            }
        }
        if ((pos.j == row_length - 2) or (field_array[pos.i + (pos.j + 1) * row_length] != current_val)) {
            const prev_pos = Position{ .i = pos.i - 1, .j = pos.j };
            const prev_val = field_array[prev_pos.i + prev_pos.j * row_length];
            if (pos.i == 0 or !(prev_val == current_val and ((prev_pos.j == row_length - 2) or (field_array[prev_pos.i + (prev_pos.j + 1) * row_length] != current_val)))) {
                perimeter += 1;
            }
        }

        return perimeter;
    }
};

const Region = struct {
    area: i64,
    perimeter: i64,
};

fn run(input: [:0]const u8) i64 {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const total_length: f32 = @floatFromInt(input.len);
    const length: usize = @intFromFloat(@sqrt(total_length) + 1);

    var region_list = std.ArrayList(Region).init(allocator);
    var region_array = allocator.alloc(?usize, length * length) catch unreachable;
    var region_count: usize = 0;

    for (0..length - 1) |j| {
        for (0..length - 1) |i| {
            const current_pos: Position = .{ .i = i, .j = j };
            const perimeter = current_pos.get_perimeter(input, length);
            const check_result = current_pos.check_before(input, region_array, length);
            switch (check_result) {
                CheckResultTag.region_num => |region_num| {
                    region_list.items[region_num].area += 1;
                    region_list.items[region_num].perimeter += perimeter;
                    current_pos.set_val(?usize, region_num, &region_array, length);
                },
                CheckResultTag.no_region => {
                    region_list.append(Region{ .perimeter = perimeter, .area = 1 }) catch unreachable;
                    current_pos.set_val(?usize, region_count, &region_array, length);
                    region_count += 1;
                },
                CheckResultTag.region_pair => |region_pair| {
                    region_list.items[region_pair.first_region].perimeter += region_list.items[region_pair.second_region].perimeter;
                    region_list.items[region_pair.first_region].area += region_list.items[region_pair.second_region].area;
                    region_list.items[region_pair.second_region].perimeter = 0;
                    region_list.items[region_pair.second_region].area = 0;
                    for (region_array, 0..) |value, k| {
                        if (value == region_pair.second_region) {
                            region_array[k] = region_pair.first_region;
                        }
                    }
                    region_list.items[region_pair.first_region].area += 1;
                    region_list.items[region_pair.first_region].perimeter += perimeter;
                    current_pos.set_val(?usize, region_pair.first_region, &region_array, length);
                },
            }
        }
    }

    var total: i64 = 0;
    for (region_list.items) |region| {
        total += region.area * region.perimeter;
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
