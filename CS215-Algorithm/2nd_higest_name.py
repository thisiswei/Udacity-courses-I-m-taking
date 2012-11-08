


file = open('yob1995.txt','r')

max_name = 'none'
max_val = 0
sec_name = 'none'
sec_val = 0


for line in f:
    (name,sex,count) = line.rsplit(',')
    count = int(count)
    if sex == 'F' :
        if count > max_val :
            sec_val = max_val
            sec_name = max_name
            max_val = count 
            max_name = name
        elif count > sec_val:
            sec_val = count
            sec_name = name

print sec_name
print sec_val
