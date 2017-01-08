import sys
from pattern_matcher import PatternMatcher, PatternNode


if __name__ == '__main__':
    _input = map(lambda line: line.rstrip('\n') , sys.stdin)

    total_patterns = int(_input[0])
    patterns = _input[1 : total_patterns + 1]
    pattern_matcher = PatternMatcher()
    for pattern in patterns:
        pattern_matcher.insert(pattern)

    total_paths = int(_input[total_patterns+1])
    path_starts = total_patterns + 2
    path_ends = path_starts + total_paths
    paths = map(lambda path: path.strip('/'), _input[path_starts : path_ends])
    for path in paths:
        print pattern_matcher.find_match(path)
