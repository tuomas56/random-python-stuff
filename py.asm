py_binary_sub:
	pop ecx
	pop eax
	sub eax,ecx
	push eax
	ret

py_binary_add:
	pop ecx
	pop eax
	add eax,ecx
	push eax
	ret

py_binary_modulo:
	pop ecx
	pop eax
	div ecx
	push edx
	ret

py_binary_true_divide:
	pop ecx
	pop eax
	div ecx
	push eax
	ret

py_binary_floor_divide:
	pop ecx
	pop eax
	div ecx
	push eax
	ret

py_binary_multiply:
	pop ecx
	pop eax
	mul ecx
	push eax
	ret

py_binary_power:
	pop ecx
	pop eax
	mov edx,ecx
.py_binary_power_0:
	cmp ecx, 0
	je .py_binary_power_1
	mul edx
	dec ecx
	jmp .py_binary_power_0
.py_binary_power_1
	push eax
	ret


py_unary_invert:
	pop eax
	neg eax
	push eax
	ret

py_unary_not:
	pop eax
	not eax
	push eax
	ret

py_unary_negative:
	pop eax
	mov ecx, eax
	shr ecx, 31
	xor eax,ecx
	sub eax,ecx
	neg eax
	push eax
	ret

py_unary_positive:
	pop eax
	mov ecx, eax
	shr ecx, 31
	xor eax, ecx
	sub eax, ecx
	push eax
	ret

py_rot_three:
	pop eax
	pop ecx
	pop edx
	push eax
	push edx
	push ecx
	ret

py_rot_two:
	pop eax
	pop ecx
	push eax
	push ecx
	ret

py_pop_top:
	pop ax
	ret

py_nop:
	nop
	ret