n = int(input())
heights = list(map(int, input().split()))
roof_panels = sum(1 for h in heights if h > 0)

side_panels = sum(abs(heights[i] - heights[i - 1]) for i in range(1, len(heights)))

side_panels += heights[0] + heights[-1]
print(roof_panels + side_panels)
