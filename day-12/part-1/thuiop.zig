const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

var region_list: [5000]Region = undefined;

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

fn Grid(comptime T: type) type {
    return struct {
        array: []T,
        row_length: usize,

        const Self = @This();

        fn init(row_length: usize, alloc: std.mem.Allocator) Self {
            const array = alloc.alloc(T, row_length * row_length) catch unreachable;
            return .{
                .array = array,
                .row_length = row_length,
            };
        }

        fn get(self: Self, pos: Position) T {
            return self.array[pos.i + self.row_length * pos.j];
        }

        fn set(self: Self, pos: Position, value: T) void {
            self.array[pos.i + self.row_length * pos.j] = value;
        }

        fn replace(self: Self, value: T, by: T, lim: usize) void {
            for (self.array[0..lim], 0..) |x, k| {
                if (x == value) {
                    self.array[k] = by;
                }
            }
        }
    };
}

const Direction = enum(u2) {
    North,
    East,
    South,
    West,
};

const Position = struct {
    i: usize,
    j: usize,

    fn is_not_out(pos: Position, length: usize) bool {
        return pos.i >= 0 and pos.i <= length - 1 and pos.j >= 0 and pos.j <= length - 1;
    }

    fn next(self: Position, dir: Direction) Position {
        return switch (dir) {
            Direction.East => Position{ .i = self.i + 1, .j = self.j },
            Direction.West => Position{ .i = self.i - 1, .j = self.j },
            Direction.South => Position{ .i = self.i, .j = self.j + 1 },
            Direction.North => Position{ .i = self.i, .j = self.j - 1 },
        };
    }

    fn check_before(current_pos: Position, field_grid: Grid(u8), region_grid: Grid(usize)) CheckResult {
        const current_val = field_grid.get(current_pos);
        const west_pos = if (current_pos.i > 0) current_pos.next(.West) else null;
        const north_pos = if (current_pos.j > 0) current_pos.next(.North) else null;
        var regions: [2]usize = undefined;
        var region_count: u8 = 0;
        inline for (.{ west_pos, north_pos }) |pos| {
            if (pos) |pos_unwrap| {
                if (field_grid.get(pos_unwrap) == current_val) {
                    regions[region_count] = region_grid.get(pos_unwrap);
                    region_count += 1;
                }
            }
        }
        return switch (region_count) {
            0 => CheckResult.no_region,
            1 => CheckResult{ .region_num = regions[0] },
            2 => if (regions[0] != regions[1]) CheckResult{ .region_pair = RegionPair{ .first_region = regions[0], .second_region = regions[1] } } else CheckResult{ .region_num = regions[0] },
            else => unreachable,
        };
    }

    inline fn first_cond(current_val: u8, current_pos: Position, dir: Direction, field_grid: Grid(u8)) bool {
        var ok: bool = switch (dir) {
            .West => current_pos.i == 0,
            .East => current_pos.i == field_grid.row_length - 1,
            .North => current_pos.j == 0,
            .South => current_pos.j == field_grid.row_length - 1,
        };
        if (!ok) {
            ok = field_grid.get(current_pos.next(dir)) != current_val;
        }
        return ok;
    }

    fn get_perimeter(current_pos: Position, field_grid: Grid(u8)) i64 {
        const current_val = field_grid.get(current_pos);
        var perimeter: i64 = 0;
        inline for ([4]Direction{ .North, .South, .West, .East }) |dir| {
            if (first_cond(current_val, current_pos, dir, field_grid)) {
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
    const allocator = arena.allocator();

    var it = std.mem.splitScalar(u8, input, "\n"[0]);
    const row_length = it.peek().?.len;

    var region_grid = Grid(usize).init(row_length, allocator);
    @memset(region_grid.array, 0);

    const field_grid = Grid(u8).init(row_length, allocator);

    var row_count: usize = 0;
    while (it.next()) |row| {
        if (row.len == 0) {
            break;
        }
        @memcpy(field_grid.array[row_count * row_length .. (row_count + 1) * row_length], row);
        row_count += 1;
    }

    var region_count: usize = 0;

    for (0..row_length) |j| {
        for (0..row_length) |i| {
            const current_pos: Position = .{ .i = i, .j = j };
            const perimeter = current_pos.get_perimeter(field_grid);
            const check_result = current_pos.check_before(field_grid, region_grid);
            switch (check_result) {
                CheckResultTag.no_region => {
                    region_list[region_count] = Region{ .perimeter = perimeter, .area = 1 };
                    region_grid.set(current_pos, region_count);
                    region_count += 1;
                },
                CheckResultTag.region_num => |region_num| {
                    region_list[region_num].area += 1;
                    region_list[region_num].perimeter += perimeter;
                    region_grid.set(current_pos, region_num);
                },
                CheckResultTag.region_pair => |region_pair| {
                    region_list[region_pair.first_region].perimeter += region_list[region_pair.second_region].perimeter + perimeter;
                    region_list[region_pair.first_region].area += region_list[region_pair.second_region].area + 1;
                    region_list[region_pair.second_region].perimeter = 0;
                    region_list[region_pair.second_region].area = 0;
                    region_grid.replace(region_pair.second_region, region_pair.first_region, current_pos.i + row_length * j);
                    region_grid.set(current_pos, region_pair.first_region);
                },
            }
        }
    }

    var total: i64 = 0;
    for (region_list[0..region_count]) |region| {
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
