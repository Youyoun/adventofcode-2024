const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn findXmasAt(grid: Grid(u8), x: isize, y: isize) i64 {
    var count: i64 = 0;
    if (grid.atOrDot(x, y) != 'X') return 0;
    // Horizontal
    if (grid.atOrDot(x + 1, y) == 'M' and grid.atOrDot(x + 2, y) == 'A' and grid.atOrDot(x + 3, y) == 'S') {
        count += 1;
    }
    if (grid.atOrDot(x - 1, y) == 'M' and grid.atOrDot(x - 2, y) == 'A' and grid.atOrDot(x - 3, y) == 'S') {
        count += 1;
    }
    // Vertical
    if (grid.atOrDot(x, y + 1) == 'M' and grid.atOrDot(x, y + 2) == 'A' and grid.atOrDot(x, y + 3) == 'S') {
        count += 1;
    }
    if (grid.atOrDot(x, y - 1) == 'M' and grid.atOrDot(x, y - 2) == 'A' and grid.atOrDot(x, y - 3) == 'S') {
        count += 1;
    }
    // Diagonal
    if (grid.atOrDot(x + 1, y + 1) == 'M' and grid.atOrDot(x + 2, y + 2) == 'A' and grid.atOrDot(x + 3, y + 3) == 'S') {
        count += 1;
    }
    if (grid.atOrDot(x - 1, y - 1) == 'M' and grid.atOrDot(x - 2, y - 2) == 'A' and grid.atOrDot(x - 3, y - 3) == 'S') {
        count += 1;
    }
    if (grid.atOrDot(x + 1, y - 1) == 'M' and grid.atOrDot(x + 2, y - 2) == 'A' and grid.atOrDot(x + 3, y - 3) == 'S') {
        count += 1;
    }
    if (grid.atOrDot(x - 1, y + 1) == 'M' and grid.atOrDot(x - 2, y + 2) == 'A' and grid.atOrDot(x - 3, y + 3) == 'S') {
        count += 1;
    }

    return count;
}

fn run(input: [:0]const u8) i64 {
    var data = std.ArrayList(u8).init(a);
    var width: usize = 0;
    var first: bool = true;
    for (input, 0..) |c, i| {
        if (c == '\n') {
            if (first) {
                first = false;
                width = i;
            }
            continue;
        }
        data.append(c) catch unreachable;
    }
    const grid = Grid(u8){ .width = width, .height = data.items.len / width, .data = data.items };

    var result: i64 = 0;
    for (0..grid.height) |y| {
        for (0..grid.width) |x| {
            const xi: isize = @intCast(x);
            const yi: isize = @intCast(y);
            result += findXmasAt(grid, xi, yi);
        }
    }
    // your code here
    return result;
}

pub fn Grid(comptime T: type) type {
    return struct {
        width: usize,
        height: usize,
        data: []T,

        pub fn at(self: @This(), x: isize, y: isize) ?T {
            if (x < 0 or x >= @as(isize, @intCast(self.width))) return null;
            if (y < 0 or y >= @as(isize, @intCast(self.height))) return null;
            const xu: usize = @intCast(x);
            const yu: usize = @intCast(y);
            return self.data[yu * self.width + xu];
        }

        pub fn atOrDot(self: @This(), x: isize, y: isize) T {
            return self.at(x, y) orelse '.';
        }
    };
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
        \\MMMSXXMASM
        \\MSAMXMSMSA
        \\AMXSXMAAMM
        \\MSAMASMSMX
        \\XMASAMXAMM
        \\XXAMMXXAMA
        \\SMSMSASXSS
        \\SAXAMASAAA
        \\MAMMMXMMMM
        \\MXMXAXMASX
    ;

    const result = run(input);
    try std.testing.expectEqual(@as(i64, 18), result);
}
