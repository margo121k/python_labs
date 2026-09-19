string = input()
ind_first_letter = ind_second_letter = 0
for i in range(len(string)): #находим индекс 1 буквы
    if string[i].isupper():
        ind_first_letter = i
        break
for i in range(ind_first_letter, len(string)): #находим индекс 2 буквы
    if string[i].isdigit():
        ind_second_letter = i+1
        break
character_spacing = ind_second_letter - ind_first_letter #находим межсимвольный интервал
source_string = ""
ind = ind_first_letter
while string[ind]!='.': #пока не встретилась точка, собираем исходную строку с интервалом
    source_string+=string[ind]
    ind+=character_spacing
print(source_string+'.')