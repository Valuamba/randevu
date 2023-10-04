class Solution:
   def solve(self, nums):
      count = 0
      ans = 0
      for i in range(2, len(nums)):
         if nums[i] - nums[i - 1] == nums[i - 1] - nums[i - 2]:
            count += 1
         else:
            ans += (count * (count + 1)) // 2
            count = 0
      if count:
         ans += (count * (count + 1)) // 2
      return ans

ob = Solution()


nums = list(set([6, 8, 10, 12, 13, 14, 16, 17, 20, 21, 23, 24, 25]))


duration = 3

out = []

for i in range(len(nums)):
    counter = 0

    if len(nums) < i + duration:
      continue

    for j in range(i, i + duration - 1):
        if nums[j + 1] - nums[j] == 1:
            counter += 1
        else:
            break

    if counter >= duration - 1:
        out.append(nums[i])


print(out)

# print(ob.solve(nums))