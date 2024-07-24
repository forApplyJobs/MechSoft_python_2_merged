def find_max(t, z):
    max_value = 0
    for i in range(len(t)):
        for j in range(i + 1, len(t) + 1):
            substring = t[i:j]
            count = z.count(substring)
            value = len(substring) * count
            if value > max_value:
                max_value = value                
    return max_value
if __name__ == '__main__':
    t = "acldm1labcdhsnd"
    z = "shabcdacasklksjabcdfueuabcdfhsndsabcdmdabcdfa"
    print(find_max(t, z))  
