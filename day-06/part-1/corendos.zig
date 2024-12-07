const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

pub fn Grid(comptime T: type) type {
    return struct {
        width: usize,
        height: usize,
        data: []T,

        pub fn at(self: @This(), x: isize, y: isize) ?*T {
            if (x < 0 or x >= @as(isize, @intCast(self.width))) return null;
            if (y < 0 or y >= @as(isize, @intCast(self.height))) return null;
            const xu: usize = @intCast(x);
            const yu: usize = @intCast(y);
            return &self.data[yu * self.width + xu];
        }
    };
}

pub const Cell = enum {
    empty,
    obstacle,
};

pub const Orientation = enum {
    up,
    down,
    left,
    right,

    pub fn turn(self: Orientation) Orientation {
        return switch (self) {
            .up => .right,
            .down => .left,
            .left => .up,
            .right => .down,
        };
    }
};

fn run(input: [:0]const u8) i64 {
    var data = std.ArrayList(Cell).init(a);
    var width: usize = 0;
    var first: bool = true;
    var guard_x: i64 = 0;
    var guard_y: i64 = 0;
    var x: i64 = 0;
    var y: i64 = 0;
    var orientation: Orientation = .up;
    for (input, 0..) |c, i| {
        if (c == '\n') {
            if (first) {
                first = false;
                width = i;
            }
            y += 1;
            x = 0;
            continue;
        }
        switch (c) {
            '#' => data.append(.obstacle) catch unreachable,
            '.' => data.append(.empty) catch unreachable,
            '^' => {
                guard_x = x;
                guard_y = y;
                data.append(.empty) catch unreachable;
            },
            else => unreachable,
        }
        x += 1;
    }
    const grid = Grid(Cell){ .width = width, .height = data.items.len / width, .data = data.items };
    var visited_data = a.alloc(bool, grid.width * grid.height) catch unreachable;
    @memset(visited_data, false);
    visited_data[@as(usize, @intCast(guard_y)) * width + @as(usize, @intCast(guard_x))] = true;
    const visited_grid = Grid(bool){ .width = width, .height = grid.height, .data = visited_data };

    while (true) {
        const new_x, const new_y = switch (orientation) {
            .up => .{ guard_x, guard_y - 1 },
            .down => .{ guard_x, guard_y + 1 },
            .left => .{ guard_x - 1, guard_y },
            .right => .{ guard_x + 1, guard_y },
        };
        if (new_x < 0 or new_x >= width or new_y < 0 or new_y >= grid.height) break;
        if (grid.at(new_x, new_y).?.* == .obstacle) {
            orientation = orientation.turn();
            continue;
        }
        guard_x = new_x;
        guard_y = new_y;
        visited_grid.at(guard_x, guard_y).?.* = true;
    }

    var result: i64 = 0;
    for (visited_grid.data) |v| {
        if (v) result += 1;
    }

    // your code here
    return result;
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

test "example" {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings

    defer arena.deinit(); // clear memory
    a = arena.allocator();

    const input =
        \\....#.....
        \\.........#
        \\..........
        \\..#.......
        \\.......#..
        \\..........
        \\.#..^.....
        \\........#.
        \\#.........
        \\......#...
    ;

    const result = run(input);
    try std.testing.expectEqual(@as(i64, 41), result);
}
