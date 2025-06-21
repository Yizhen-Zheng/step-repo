class Solution:
    def solution(self, s: str) -> int:
        '''
        input: 
        GGWW
        GWWGGWGWG
        find min number of changes (G->W or W->G)to make to convert the string into all G are in left side and all W are in right side
        better solution:
        use a spliting line and sliding through the string (O(N))
        the line represent:
        in the left of the line, all W should be convert to G
        in the right of the line, all G should be convert to W
        '''
        if len(s) <= 1:
            return 0
        length = len(s)
        # O(N) to count G
        count = s.count('G')
        ans = count
        # initial situations: line is in left most, so all the G should be changed to W
        line = 0
        # slide the line into right
        while line < length:
            # each step would put current char into left side
            if s[line] == 'G':
                count -= 1
                ans = min(ans, count)
            else:
                count += 1
            line += 1
        return ans


# t = 'GWGWGWGGGGGWWWGGGGGGWGGWGGWWWWWGGWWWGWGWWGWWWGWWGWWWGGGGGWWWWGGGGWWWWG'
# t = 'WWWGG'
t = 'GG'
# t = 'WW'

ans = Solution().solution(t)

print(ans)
'''
while idx<len and white-broccoli-left!=0
(If only green broccoli, return 0 directly)
If current is white,white broccoli left-=1, idx+=1
If current is green,count +=1
Return count
'''
