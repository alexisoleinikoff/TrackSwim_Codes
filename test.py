a = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
j = 0
z = len(a)

while j < z:
	if j == 0:
		for x in range(z):
			if x != z-1:
				print(a[x], end =" ")
			else:
				print(a[x])
	else:
		print(a[j]+" "*(j*2 -1)+a[j])
	j += 1
