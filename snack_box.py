# 간식박스 관리 프로그램 1
snack_box = ['초코파이']
new_snack = input('먹고 싶은 간식을 추가하세요.  단, 쉼표(,)로 연결하세요').split(',')
snack_box += new_snack


snack_box


qty=int(input('간식박스를 몇 세트로 포장할까요? 예:2->2box'))

snack_box*=qty
snack_box
print(f'주문하신 간식상자는 {snack_box[0]},{snack_box[1]},{snack_box[2]} 등입니다. 확인해주세요')


msg=f'혹시 빼고싶은 간식이 있으면 번호를 입력하세요(0~{len(snack_box)-1})'
snack_no=int(input(msg))

del snack_box[snack_no]

snack_name=input('찾고 싶은 간식을 입력하세요')
if snack_name in snack_box:
    print('있어요')
else:
    print('없어요')

    #간식박스 관리 프로그램5
print('주문하신 간식박스는 뒤에서부터 다음과 같습니다.')
print(snack_box[::-1])
print(f'{snack_box[::-1]},총 {len(snack_box)}개')