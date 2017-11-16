import random
cards = ['As',2,3,4,5,6,7,8,9,10,'J','Q','K']
nums = {}
for i in range(13):
    nums[i+1]=cards[i]
    nums[cards[i]]=i+1
cards = 4*cards
score = 0
index = random.randint(0,len(cards)-1)
current = cards[index]
print(current)
del cards[index]
last = nums[current]
while len(cards) > 0:
    print("Score:",score)
    temp = 0
    for i in range(1,nums[current]-1):
        temp += cards.count(nums[i+1])
    print(float(temp)/float(len(cards)))
    move = input()
    index = random.randint(0,len(cards)-1)
    current = cards[index]
    if nums[current] == 1:
        print(current)
        index = random.randint(0,len(cards)-1)
        current = cards[index]
        print(current)
    elif ((move == '+' and last >= nums[current]) or (move == '-' and last <= nums[current])):
        score += 1
    del cards[index]
    print("Current:",current,"Last:",nums[last])
    last = nums[current]
