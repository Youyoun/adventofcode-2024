const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const User = struct {
    name: u16,
    links: *std.ArrayList(u16),
    done: bool = false,
};

fn run(input: [:0]const u8) i64 {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    const allocator = arena.allocator();

    var it = std.mem.splitScalar(u8, input, "\n"[0]);
    var user_map = std.AutoHashMap(u16, User).init(allocator);

    while (it.next()) |row| {
        const first: u16 = @bitCast(row[0..2].*);
        const second: u16 = @bitCast(row[3..5].*);

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

    var result: i64 = 0;
    var map_it = user_map.valueIterator();
    while (map_it.next()) |user1| {
        const start_t_1 = user1.name % 256 == "t"[0];
        for (user1.links.items) |username2| {
            const user2 = user_map.get(username2).?;
            if (user2.done) {
                continue;
            }
            const start_t_2 = username2 % 256 == "t"[0];
            inner: for (user1.links.items) |username3| {
                if (user_map.get(username3).?.done) {
                    continue;
                }
                const start_t_3 = username3 % 256 == "t"[0];
                for (user2.links.items) |username4| {
                    if (username3 == username4 and (start_t_1 or start_t_2 or start_t_3)) {
                        result += 1;
                        continue :inner;
                    }
                }
            }
        }
        user1.done = true;
    }

    return @divTrunc(result, 2);
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
