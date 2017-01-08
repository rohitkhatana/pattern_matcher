class PatternNode:

    def __init__(self, pattern):
        self.left = None
        self.right = None
        self.patterns = []
        self.patterns.append(pattern)
        self.size = len(pattern)

    def is_leaf_node(self):
        return self.left == None and self.right == None

class PatternMatcher:

    WILDCARD = "*"

    def __init__(self):
        self.root = None

    def insert(self, pattern):
        pattern = pattern.split(',')
        if self.root is None:
            self.root = PatternNode(pattern)
        else:
            self.__insert_child_node(self.root, pattern)

    def __insert_child_node(self, current, pattern):
        len_pattern = len(pattern)
        if len_pattern < current.size:
            if current.left == None:
                current.left = PatternNode(pattern)
            else:
                self.__insert_child_node(current.left, pattern)
        elif len_pattern > current.size:
            if current.right == None:
                current.right = PatternNode(pattern)
            else:
                self.__insert_child_node(current.right, pattern)
        else:
            current.patterns.append(pattern)


    def __best_match(self, matches, best_match_index):
        best_patterns = []
        for match in matches:
            for index in xrange(best_match_index, len(match)):
                current_letter = match[index]
                if current_letter == self.WILDCARD:
                    left_index = index
                    if left_index > best_match_index:
                        best_match_index = left_index
                        best_patterns = [match]
                    elif left_index == best_match_index:
                        best_patterns.append(match)
                    break
        if len(best_patterns) == 1:
            return best_patterns[0]
        else:
            return self.__best_match(best_patterns, best_match_index+1)

    def __sort_by_wildcard_count(self, matches):
        return sorted(matches, key=lambda x: x.count(self.WILDCARD))

    def __min_wildcard_count(self, matches):
        matches = self.__sort_by_wildcard_count(matches)
        if matches[0].count(self.WILDCARD) < matches[1].count(self.WILDCARD):
            return matches[0]
        else:
            return None

    def find_match(self, path):
        path = path.split('/')
        if path[-1] == '':
            path = path[:-1]

        matches = self.__find(self.root, path, [])
        if len(matches) > 1:
            return ','.join(self.__min_wildcard_count(matches) or self.__best_match(matches, 0))
        elif len(matches) == 1:
            return ','.join(matches[0])
        else:
            return "NO MATCH"

    def __find(self, current, path, matches):
        if current.size > len(path) and current.left != None:
            return self.__find(current.left, path, matches)
        elif current.size < len(path) and current.right != None:
            return self.__find(current.right, path, matches)
        elif current.size == len(path):
            for pattern in current.patterns:
                found = True
                for i in range(len(path)):
                    if path[i] != pattern[i] and pattern[i] != self.WILDCARD:
                        found = False
                if found:
                    matches.append(pattern)
            return matches
        else:
            return []
