const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

var ar = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings
const allocator = ar.allocator();

const Direction = enum(u2) {
    Left,
    Right,
    Up,
    Down,
};

fn new_direction(dir: Direction) Direction {
    return switch (dir) {
        .Up => Direction.Right,
        .Right => Direction.Down,
        .Down => Direction.Left,
        .Left => Direction.Up,
    };
}

fn GridWithDir(comptime T: type) type {
    return struct {
        array: []T,
        row_length: usize,

        const Self = @This();
        fn get(self: Self, pos: Position) T {
            return self.array[pos.i + pos.j * self.row_length + @intFromEnum(pos.dir) * self.row_length * self.row_length];
        }

        fn set(self: Self, pos: Position, val: T) void {
            self.array[pos.i + pos.j * self.row_length + @intFromEnum(pos.dir) * self.row_length * self.row_length] = val;
        }
    };
}

fn Grid(comptime T: type) type {
    return struct {
        array: []T,
        row_length: usize,

        const Self = @This();
        fn get(self: Self, pos: Position) T {
            return self.array[pos.i + pos.j * self.row_length];
        }

        fn set(self: Self, pos: Position, val: T) void {
            self.array[pos.i + pos.j * self.row_length] = val;
        }

        fn grid_print(self: Self) void {
            for (0..self.row_length) |i| {
                std.debug.print("{any}\n", .{self.array[i * self.row_length .. (i + 1) * self.row_length]});
            }
        }
    };
}

const Position = struct {
    i: usize,
    j: usize,
    dir: Direction,

    fn get_next(pos: Position, dir: Direction) Position {
        var new_pos: Position = .{ .i = pos.i, .j = pos.j, .dir = dir };
        switch (dir) {
            .Up => new_pos.j -= 1,
            .Down => new_pos.j += 1,
            .Left => new_pos.i -= 1,
            .Right => new_pos.i += 1,
        }
        return new_pos;
    }

    fn is_not_out(pos: Position, length: usize) bool {
        return pos.i != 0 and pos.i != length - 2 and pos.j != 0 and pos.j != length - 2;
    }
};

fn try_obstacle(grid: Grid(u8), visited_grid: GridWithDir(bool), new_visited_grid: GridWithDir(bool), initial_pos: Position) bool {
    var pos = initial_pos;
    @memcpy(new_visited_grid.array, visited_grid.array);

    while (pos.is_not_out(grid.row_length)) {
        if (new_visited_grid.get(pos)) {
            return true;
        } else {
            new_visited_grid.set(pos, true);
        }
        const new_pos = pos.get_next(pos.dir);
        if (grid.get(new_pos) == "#"[0]) {
            pos.dir = new_direction(pos.dir);
        } else {
            pos = new_pos;
        }
    }
    return false;
}

fn run(input: [:0]const u8) i64 {
    const total_length: f32 = @floatFromInt(input.len);
    const row_length: usize = @intFromFloat(@sqrt(total_length) + 1);

    const initial_index = std.mem.indexOf(u8, input, "^").?;
    var pos: Position = .{ .i = initial_index % row_length, .j = initial_index / row_length, .dir = Direction.Up };

    const grid = Grid(u8){ .array = @constCast(input), .row_length = row_length };

    var visited_grid = GridWithDir(bool){ .array = allocator.alloc(bool, row_length * row_length * 4) catch unreachable, .row_length = row_length };
    const new_visited_grid = GridWithDir(bool){ .array = allocator.alloc(bool, row_length * row_length * 4) catch unreachable, .row_length = row_length };
    var obstacle_tried_grid = Grid(bool){ .array = allocator.alloc(bool, row_length * row_length) catch unreachable, .row_length = row_length };
    var new_obstacle_count: i64 = 0;

    while (pos.is_not_out(row_length)) {
        if (!visited_grid.get(pos)) {
            visited_grid.set(pos, true);
        }
        const new_pos = pos.get_next(pos.dir);
        if (grid.get(new_pos) == "#"[0]) {
            pos.dir = new_direction(pos.dir);
        } else {
            if (!obstacle_tried_grid.get(new_pos)) {
                grid.set(new_pos, "#"[0]);
                new_obstacle_count += @intFromBool(try_obstacle(grid, visited_grid, new_visited_grid, Position{ .i = pos.i, .j = pos.j, .dir = new_direction(pos.dir) }));
                grid.set(new_pos, "."[0]);
                obstacle_tried_grid.set(new_pos, true);
            }
            pos = new_pos;
        }
    }
    return new_obstacle_count;
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
