const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

var ar = std.heap.ArenaAllocator.init(std.heap.page_allocator);
const allocator = ar.allocator();

const User = struct {
    name: u16,
    links: *std.ArrayList(u16),
    visited: bool = false,
};

fn run(input: [:0]const u8) []u8 {
    var it = std.mem.splitScalar(u8, input, "\n"[0]);
    var user_map = std.AutoHashMap(u16, User).init(allocator);

    while (it.next()) |row| {
        const first: u16 = @as(u16, row[0]) * 256 + @as(u16, row[1]);
        const second: u16 = @as(u16, row[3]) * 256 + @as(u16, row[4]);

        const first_user_result = user_map.getOrPut(first) catch unreachable;
        if (first_user_result.found_existing) {
            first_user_result.value_ptr.links.append(second) catch unreachable;
        } else {
            var new_list = allocator.create(std.ArrayList(u16)) catch unreachable;
            new_list.* = std.ArrayList(u16).init(allocator);
            new_list.append(second) catch unreachable;
            first_user_result.value_ptr.* = User{ .name = first, .links = new_list };
        }

        const second_user_result = user_map.getOrPut(second) catch unreachable;
        if (second_user_result.found_existing) {
            second_user_result.value_ptr.links.append(first) catch unreachable;
        } else {
            var new_list = allocator.create(std.ArrayList(u16)) catch unreachable;
            new_list.* = std.ArrayList(u16).init(allocator);
            new_list.append(first) catch unreachable;
            second_user_result.value_ptr.* = User{ .name = second, .links = new_list };
        }
    }

    var map_it = user_map.valueIterator();
    var result: []u8 = undefined;
    var current_max_len: usize = 0;
    while (map_it.next()) |user| {
        if (!user.visited) {
            var clique = allocator.create(std.ArrayList(u16)) catch unreachable;
            clique.* = std.ArrayList(u16).init(allocator);
            clique.append(user.name) catch unreachable;
            var map_it2 = user_map.valueIterator();
            outer: while (map_it2.next()) |new_user| {
                for (clique.items) |clique_user| {
                    var ok = false;
                    for (new_user.links.items) |possible_match| {
                        if (possible_match == clique_user) {
                            ok = true;
                            break;
                        }
                    }
                    if (!ok) {
                        continue :outer;
                    }
                }
                clique.append(new_user.name) catch unreachable;
                new_user.visited = true;
            }
            if (clique.items.len > current_max_len) {
                current_max_len = clique.items.len;
                std.mem.sort(u16, clique.items, {}, std.sort.asc(u16));
                result = allocator.alloc(u8, clique.items.len * 3 - 1) catch unreachable;
                for (0..clique.items.len, clique.items) |i, username| {
                    result[3 * i] = @intCast(username / 256);
                    result[3 * i + 1] = @intCast(username % 256);
                    if (i < clique.items.len - 1) {
                        result[3 * i + 2] = ","[0];
                    }
                }
            }
        }
    }
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
    try stdout.print("_duration:{d}\n{s}\n", .{ elapsed_milli, answer }); // emit actual lines parsed by AOC
}
